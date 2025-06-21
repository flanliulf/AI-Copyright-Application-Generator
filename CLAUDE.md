# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains an **AI-driven Software Copyright Application Materials Generation System**. The system is designed to automatically generate complete documentation and code materials required for software copyright registration by providing necessary project requirements and technical specifications.

### Core System Components

The system consists of three main generation modules:

1. **Documentation Generation Module** - Automated creation of technical documentation and design specifications
2. **Source Code Generation Module** - Complete frontend and backend code generation for copyright submission
3. **Copyright Application Materials Module** - Specialized documents for software copyright registration process

### Key Features

- **Automated Material Generation**: Complete software copyright application materials from basic requirements
- **AI-Powered Code Creation**: Full-stack source code generation for copyright verification
- **Multiple UI Design Styles**: Three professional UI design options (Corporate, Cyberpunk, Minimal) with intelligent selection
- **User-Friendly Project Initialization**: Interactive setup with guided UI style selection and configuration
- **Standardized Documentation**: Professional technical documents meeting copyright office requirements
- **Multi-Format Output**: Generates code files, documentation, and application forms in required formats
- **Compliance Assurance**: Ensures all materials meet software copyright registration standards

### System Architecture

The system utilizes the following AI-driven generation framework:
- AI/LLM services for automated code and documentation generation
- Systematic prompt engineering for consistent output quality
- Template-based generation ensuring copyright compliance standards
- Multi-stage workflow for comprehensive material creation
- Quality assurance mechanisms for professional deliverables

### Development Context

This repository contains a complete software copyright materials generation framework:
- **requires_docs/**: Input requirements and technical specifications for any software project
- **output_docs/**: Generated copyright application materials (technical docs, user manuals, registration forms)
- **output_sourcecode/**: Complete generated source code for copyright submission
- **specs_docs/**: Fixed specification documents and templates for consistent generation
  - **ui_design_specs/**: Three professional UI design specifications (Corporate, Cyberpunk, Minimal)
  - **tech_stack_specs/**: Default technology stack templates
- **system_prompts/**: Seven specialized AI prompts for different generation stages
- **workflow documentation**: Step-by-step process for generating complete copyright materials

The system can process any software project requirements to generate complete copyright application packages with professional UI designs tailored to different application types.

### Important Notes

- Generated materials must comply with software copyright office requirements and standards
- All AI-generated content should be reviewed for accuracy and completeness before submission
- The system supports various software types and technical stacks for broad applicability
- Output materials are formatted specifically for copyright registration processes
- Quality assurance is essential for successful copyright application approval

### UI Design System

The system features three professionally designed UI styles to match different software application types:

1. **Corporate Style (Default)**: Professional business interface suitable for enterprise systems, management platforms, and government applications
2. **Cyberpunk Style**: Dark theme with technology aesthetics, ideal for developer tools, data analytics platforms, and tech-focused applications
3. **Minimal Style**: Clean and content-focused design, perfect for content management systems, educational platforms, and productivity tools

#### UI Style Selection Methods:
- **Interactive Setup**: Choose during project initialization with `python3 init_project.py`
- **Configuration**: Set `ui_design_style` parameter in `config.json`
- **Custom Override**: Create custom UI specification in `requires_docs/UI设计规范.md`

#### Priority System:
Custom UI Specification > User-Selected Style > System Default (Corporate)