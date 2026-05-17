"""
PPT Generator - SVG to native PPTX conversion
Based on ppt-master project
"""

import os
import re
import math
import base64
import io
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from xml.etree import ElementTree as ET
from dataclasses import dataclass
from PIL import Image


@dataclass
class SVGElement:
    """Represents an SVG element"""
    tag: str
    attrs: Dict
    children: List['SVGElement']
    text: str = ""
    transform: str = ""


class SVGToPPTX:
    """Convert SVG to native PPTX DrawingML"""

    # PPTX namespaces
    NS = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
        'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    }

    # Canvas formats
    CANVAS_FORMATS = {
        '16:9': (1280, 720),
        '4:3': (1024, 768),
        '小红书': (1242, 1660),
        '朋友圈': (1080, 1080),
        '抖音': (1080, 1920),
        '横版Banner': (1920, 1080),
        '竖版海报': (1080, 1920),
        'A4': (1240, 1754),
    }

    def __init__(self, canvas_width=1280, canvas_height=720):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.slides = []

    def parse_svg(self, svg_path: str) -> SVGElement:
        """Parse SVG file into element tree"""
        tree = ET.parse(svg_path)
        root = tree.getroot()
        return self._parse_element(root)

    def _parse_element(self, elem) -> SVGElement:
        """Recursively parse XML element"""
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        attrs = dict(elem.attrib)

        # Handle namespace in attributes
        if '{http://www.w3.org/2000/svg}' in elem.tag:
            tag = elem.tag.replace('{http://www.w3.org/2000/svg}', '')

        children = []
        text = elem.text or ""

        for child in elem:
            children.append(self._parse_element(child))

        return SVGElement(
            tag=tag,
            attrs=attrs,
            children=children,
            text=text,
            transform=attrs.get('transform', '')
        )

    def _parse_color(self, color_str: str) -> Optional[str]:
        """Parse color string to hex"""
        if not color_str:
            return None

        color_str = color_str.strip()

        # Hex color
        if color_str.startswith('#'):
            if len(color_str) == 4:  # #RGB
                r = color_str[1]
                g = color_str[2]
                b = color_str[3]
                return f"#{r}{r}{g}{g}{b}{b}"
            return color_str

        # RGB
        if color_str.startswith('rgb'):
            nums = re.findall(r'\d+', color_str)
            if len(nums) == 3:
                r, g, b = [int(n) for n in nums]
                return f"#{r:02x}{g:02x}{b:02x}"

        # Named colors
        named_colors = {
            'black': '#000000', 'white': '#FFFFFF', 'red': '#FF0000',
            'green': '#00FF00', 'blue': '#0000FF', 'yellow': '#FFFF00',
            'orange': '#FFA500', 'purple': '#800080', 'gray': '#808080',
        }
        return named_colors.get(color_str.lower())

    def _parse_transform(self, transform: str) -> Tuple:
        """Parse SVG transform to (translate_x, translate_y, scale_x, scale_y, rotate)"""
        tx, ty = 0, 0
        sx, sy = 1, 1
        rotation = 0

        # Translate
        match = re.search(r'translate\(([^,)]+)(?:,\s*([^)]+))?\)', transform)
        if match:
            tx = float(match.group(1))
            ty = float(match.group(2)) if match.group(2) else 0

        # Scale
        match = re.search(r'scale\(([^,)]+)(?:,\s*([^)]+))?\)', transform)
        if match:
            sx = float(match.group(1))
            sy = float(match.group(2)) if match.group(2) else sx

        # Rotate
        match = re.search(r'rotate\(([^)]+)\)', transform)
        if match:
            rotation = float(match.group(1))

        return tx, ty, sx, sy, rotation

    def _create_shape(self, element: SVGElement) -> Optional[ET.Element]:
        """Convert SVG element to PPTX shape"""
        tag = element.tag.lower()

        # Get position and dimensions
        x = float(element.attrs.get('x', 0))
        y = float(element.attrs.get('y', 0))
        width = float(element.attrs.get('width', 0))
        height = float(element.attrs.get('height', 0))

        # Parse transform
        tx, ty, sx, sy, rotation = self._parse_transform(element.transform)
        x += tx
        y += ty
        width *= sx
        height *= sy

        # Get fill and stroke
        fill = self._parse_color(element.attrs.get('fill', ''))
        stroke = self._parse_color(element.attrs.get('stroke', 'none'))
        stroke_width = float(element.attrs.get('stroke-width', 0))

        # Get text content
        text = element.text
        for child in element.children:
            if child.tag.lower() == 'tspan':
                text += child.text or ""
            text += self._get_text_recursive(child)

        shape = None

        if tag == 'rect':
            shape = self._create_rect(x, y, width, height, fill, stroke, stroke_width)
        elif tag == 'circle':
            cx = float(element.attrs.get('cx', 0))
            cy = float(element.attrs.get('cy', 0))
            r = float(element.attrs.get('r', 0))
            shape = self._create_ellipse(cx - r, cy - r, r * 2, r * 2, fill, stroke, stroke_width)
        elif tag == 'ellipse':
            cx = float(element.attrs.get('cx', 0))
            cy = float(element.attrs.get('cy', 0))
            rx = float(element.attrs.get('rx', 0))
            ry = float(element.attrs.get('ry', 0))
            shape = self._create_ellipse(cx - rx, cy - ry, rx * 2, ry * 2, fill, stroke, stroke_width)
        elif tag == 'line':
            x1 = float(element.attrs.get('x1', 0))
            y1 = float(element.attrs.get('y1', 0))
            x2 = float(element.attrs.get('x2', 0))
            y2 = float(element.attrs.get('y2', 0))
            shape = self._create_line(x1, y1, x2, y2, stroke, stroke_width)
        elif tag == 'path':
            d = element.attrs.get('d', '')
            shape = self._create_path(d, fill, stroke, stroke_width)
        elif tag == 'text':
            shape = self._create_text(x, y, width, height, text, element.attrs)
        elif tag == 'image':
            href = element.attrs.get('{http://www.w3.org/1999/xlink}href',
                                     element.attrs.get('href', ''))
            if href:
                shape = self._create_image(x, y, width, height, href)

        return shape

    def _create_rect(self, x, y, w, h, fill, stroke, stroke_width) -> ET.Element:
        """Create PPTX rectangle shape"""
        # Implementation would create proper OOXML
        pass

    def _create_ellipse(self, x, y, w, h, fill, stroke, stroke_width) -> ET.Element:
        """Create PPTX ellipse shape"""
        pass

    def _create_line(self, x1, y1, x2, y2, stroke, stroke_width) -> ET.Element:
        """Create PPTX line shape"""
        pass

    def _create_path(self, d, fill, stroke, stroke_width) -> ET.Element:
        """Create PPTX path shape"""
        pass

    def _create_text(self, x, y, w, h, text, attrs) -> ET.Element:
        """Create PPTX text box"""
        pass

    def _create_image(self, x, y, w, h, href) -> ET.Element:
        """Create PPTX image"""
        pass

    def _get_text_recursive(self, element: SVGElement) -> str:
        """Recursively get all text content"""
        text = element.text or ""
        for child in element.children:
            text += self._get_text_recursive(child)
        return text

    def convert_svg_to_pptx(self, svg_dir: str, output_path: str):
        """Convert all SVG files in directory to PPTX"""
        from pptx import Presentation
        from pptx.util import Inches, Pt

        prs = Presentation()
        prs.slide_width = Inches(self.canvas_width / 96)
        prs.slide_height = Inches(self.canvas_height / 96)

        svg_files = sorted(Path(svg_dir).glob("*.svg"))

        for svg_file in svg_files:
            slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

            # Parse and convert SVG
            svg_elem = self.parse_svg(str(svg_file))

            # Add shapes to slide
            self._add_elements_to_slide(slide, svg_elem)

        prs.save(output_path)

    def _add_elements_to_slide(self, slide, element: SVGElement):
        """Add SVG elements to PPTX slide"""
        for child in element.children:
            shape = self._create_shape(child)
            if shape:
                slide.shapes.add_shape(shape, 0, 0, 0, 0)


def create_pptx_from_svg(svg_dir: str, output_path: str, canvas_format: str = "16:9"):
    """Main entry point for SVG to PPTX conversion"""
    width, height = SVGToPPTX.CANVAS_FORMATS.get(canvas_format, (1280, 720))
    converter = SVGToPPTX(width, height)
    converter.convert_svg_to_pptx(svg_dir, output_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python svg_to_pptx.py <svg_dir> <output.pptx>")
        sys.exit(1)

    svg_dir = sys.argv[1]
    output_path = sys.argv[2]
    create_pptx_from_svg(svg_dir, output_path)
    print(f"PPTX saved to {output_path}")