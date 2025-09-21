# Smart Resume Skills Updater

An AI-powered automation tool that extracts skill requirements from job descriptions and automatically updates your resume's skills section.

## Features

- **Intelligent Skill Extraction**: Uses OpenAI GPT-4o-mini to automatically identify and classify skills from job descriptions
- **Multi-Platform Support**: Supports major ATS platforms (iCIMS, Workday, Greenhouse, Ashby, Lever, etc.)
- **Smart Classification**: Automatically categorizes skills into three main categories:
  - Programming & Frameworks
  - Software Development Tools
  - AI & Data Science
- **Automatic Resume Updates**: Directly updates Word document format resumes
- **PDF Export**: Automatically generates PDF versions of updated resumes
- **Smart Merging**: Intelligently merges new skills with existing ones, avoiding duplicates

## System Requirements

- Python 3.8+
- Microsoft Word (for PDF conversion)
- Stable internet connection

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd fetch_skills
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Playwright browser**
```bash
playwright install chromium
```

4. **Configure environment variables**
Create a `.env` file and add the following configuration:
```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Resume file paths
INPUT_RESUME=path/to/your/resume.docx
OUTPUT_RESUME=path/to/output/resume.docx

# Optional: Font and formatting configuration
FONT_NAME=Times New Roman
FONT_SIZE_PT=10.5
SPACE_AFTER_PT=6
LINE_SPACING_RULE=SINGLE
```

## Usage

### Method 1: Complete Pipeline (Recommended)
```bash
python pipeline.py "https://example.com/job-posting"
```

### Method 2: Extract Skills Only
```bash
python main.py "https://example.com/job-posting"
```

### Method 3: Update Resume Only
```bash
python update_resume.py
```

## Project Structure

```
fetch_skills/
├── main.py              # Basic skill extraction script
├── pipeline.py          # Complete automation pipeline
├── extractor.py         # Job description extractor
├── update_resume.py     # Resume update utility
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── .env                # Environment variables configuration
├── jd_text.txt         # Extracted job description text
├── output_resumes/     # Output resume directory
└── *.docx             # Resume files
```

## Supported ATS Platforms

- **iCIMS** - Popular with large enterprises
- **Workday** - Enterprise HR systems
- **Greenhouse** - Tech company favorite
- **Ashby** - Modern recruitment platform
- **Lever** - SME-friendly platform
- **SmartRecruiters** - Global recruitment platform
- **BambooHR** - SME HR systems
- **Generic Support** - Fallback mechanism for other platforms

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ | - | OpenAI API key |
| `INPUT_RESUME` | ✅ | - | Input resume file path |
| `OUTPUT_RESUME` | ✅ | - | Output resume file path |
| `FONT_NAME` | ❌ | Times New Roman | Font name |
| `FONT_SIZE_PT` | ❌ | 10.5 | Font size (points) |
| `SPACE_AFTER_PT` | ❌ | 6 | Paragraph spacing (points) |
| `LINE_SPACING_RULE` | ❌ | SINGLE | Line spacing rule |

### Resume Format Requirements

- Resume must be in `.docx` format
- Must contain "SKILLS" heading (uppercase)
- Supports skills sections in both tables and paragraphs
- Tool automatically maintains original formatting style

## Skill Classification Rules

### Programming & Frameworks
- Programming Languages: Java, Python, C++, JavaScript, etc.
- Frameworks: React, Vue.js, Spring Boot, etc.
- Development Tools: Docker, Git, Webpack, etc.

### Software Development  
- Databases: MySQL, MongoDB, Redis, etc.
- Cloud Services: AWS, Azure, GCP, etc.
- Backend Services: REST API, Microservices, etc.

### AI & Data Science
- Data Analysis: Pandas, NumPy, R, etc.
- Machine Learning: TensorFlow, PyTorch, etc.
- Visualization: Tableau, Power BI, etc.

## Important Notes

1. **API Costs**: Using OpenAI API incurs costs, monitor your usage
2. **Network Dependency**: Requires stable internet connection to access job pages
3. **File Backup**: Recommend backing up original resume files before running
4. **Format Compatibility**: Ensure resume uses standard Word format, avoid complex layouts

## Troubleshooting

### Common Issues

**Q: Unable to extract job description**
- Check if URL is accessible
- Confirm website doesn't require login
- Try accessing with different browser

**Q: Inaccurate skill extraction**
- Check if job description contains specific tech stack
- Try using more detailed job descriptions
- Consider manually adjusting extraction results

**Q: Resume update failed**
- Confirm resume file path is correct
- Check if file is being used by another program
- Verify resume format meets requirements

## Future Plans

- [ ] Support for more ATS platforms
- [ ] Add skill matching score
- [ ] Support batch processing for multiple jobs
- [ ] Add web interface
- [ ] Support more resume formats

## Contributing

Issues and Pull Requests are welcome to improve this project!

## License

MIT License

## Contact

For questions or suggestions, please contact via:
- Submit GitHub Issue
- Send email to [yangzhijiany2021@gmail.com]

---

**Note**: Please ensure compliance with relevant website terms of service and OpenAI usage policies.