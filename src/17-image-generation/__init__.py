"""
Image Generation and Editing Agent Example

This module demonstrates how to create an ADK agent specialized in image generation 
and editing using Gemini 2.5 Flash Image Preview model.

Features:
- Generate images from text descriptions
- Edit existing images with text instructions
- Upload and manage image artifacts
- Comprehensive image gallery management

The agent uses the gemini-2.5-flash-image-preview model which supports both
TEXT and IMAGE response modalities, enabling creative image generation and editing.

Usage:
    from src.image_generation.agent import image_generator
    
    # Configure with ArtifactService
    runner = Runner(
        agent=image_generator,
        app_name='image_generator',
        artifact_service=InMemoryArtifactService()
    )

Tools:
- generate_image_tool: Create images from text prompts
- edit_image_tool: Modify images based on instructions
- list_generated_images_tool: List all images by category
- show_generated_image_tool: Display specific images

Requirements:
- GOOGLE_CLOUD_API_KEY environment variable
- Access to Gemini 2.5 Flash Image Preview model
- Configured ArtifactService for image storage
"""

from .agent import image_generator, root_agent

__all__ = ["image_generator", "root_agent"]
