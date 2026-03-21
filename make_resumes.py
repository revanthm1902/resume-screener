from fpdf import FPDF

resumes = {
    "Resume_1_Revanth_StrongFit.pdf": """REVANTH MODALAVALASA
B.Tech Computer Science | Full-Stack Developer
Email: revanth@example.com

SUMMARY:
Highly motivated Computer Science undergraduate (2023-2027) with a passion for Full-Stack development, AI, and IoT. Hands-on experience building and deploying live web applications.

SKILLS:
React, Node.js, Express, MongoDB, Next.js, Vercel, Python, Java, Supabase.

EXPERIENCE & PROJECTS:
1. Second Brain (Full-Stack App)
- Built a full-stack knowledge management system using React and Node.js.
- Integrated Supabase for robust backend database management.

2. PlayNow (Web App)
- Developed a party game web application using Next.js.
- Deployed the application globally using Vercel.

3. Problem Solving
- Solved over 100 Data Structures and Algorithms problems in Java.""",

    "Resume_2_Rahul_Frontend.pdf": """RAHUL SHARMA
Web Developer
Email: rahul@example.com

SUMMARY:
Web developer focused on building beautiful, responsive user interfaces. 1 year of experience.

SKILLS:
HTML, CSS, React, JavaScript, Tailwind CSS.

EXPERIENCE:
1. E-Commerce Storefront
- Built a dynamic e-commerce frontend using React and Redux.
- Designed mobile-responsive landing pages increasing user retention by 20%.""",

    "Resume_3_Vikram_Backend.pdf": """VIKRAM SINGH
Backend Engineer
Email: vikram@example.com

SUMMARY:
Backend engineer who loves databases and scalable APIs. 2 years of experience.

SKILLS:
Node.js, Express, MongoDB, Python, SQL, AWS.

EXPERIENCE:
1. Delivery App API
- Created secure RESTful APIs using Node.js and Express for a local delivery startup.
- Managed a MongoDB database scaling to 10,000 active users.""",

    "Resume_4_Priya_Senior.pdf": """PRIYA PATEL
Principal Software Architect
Email: priya@example.com

SUMMARY:
Principal Software Architect with 12 years of experience building enterprise-grade systems.

SKILLS:
React, Node.js, Kubernetes, Docker, Microservices, C#, Azure, AWS.

EXPERIENCE:
1. Cloud Migration Lead
- Led a team of 40 engineers to migrate a legacy banking system to AWS.
- Designed distributed system architecture for a Fortune 500 company.""",

    "Resume_5_Rohan_Marketing.pdf": """ROHAN GUPTA
Digital Marketing Specialist
Email: rohan@example.com

SUMMARY:
Digital marketing specialist with a focus on SEO and performance ad campaigns.

SKILLS:
SEO, Facebook Ads, Google Analytics, Excel, Copywriting.

EXPERIENCE:
1. Growth Manager
- Increased organic website traffic by 40% through rigorous SEO optimization.
- Managed a $50k/month ad budget on Google and Meta platforms resulting in high ROI.""",

    "Resume_6_Ananya_DataScience.pdf": """ANANYA DESAI
Data Scientist
Email: ananya@example.com

SUMMARY:
Data Scientist with 3 years of experience in building machine learning models and data pipelines.

SKILLS:
Python, SQL, Pandas, Scikit-Learn, TensorFlow, Tableau.

EXPERIENCE:
1. Customer Segmentation Model
- Developed a clustering model to segment customers, improving targeted marketing by 25%.
- Built ETL pipelines to ingest and transform big data from multiple sources.""",

    "Resume_7_Kunal_UIUX.pdf": """KUNAL VERMA
UI/UX Designer
Email: kunal@example.com

SUMMARY:
Creative UI/UX Designer dedicated to crafting intuitive digital experiences.

SKILLS:
Figma, Adobe XD, Sketch, Wireframing, Prototyping, User Research.

EXPERIENCE:
1. Mobile App Redesign
- Led the complete redesign of a fintech mobile application, improving user engagement by 35%.
- Conducted comprehensive A/B testing and user research to optimize flow.""",

    "Resume_8_Sneha_PM.pdf": """SNEHA IYER
Product Manager
Email: sneha@example.com

SUMMARY:
Strategic Product Manager with 5 years of experience leading cross-functional teams to deliver software products.

SKILLS:
Agile, Scrum, Jira, Roadmap Planning, Data Analysis, Stakeholder Management.

EXPERIENCE:
1. SaaS Platform Launch
- Managed the end-to-end lifecycle of a B2B SaaS platform from ideation to launch.
- Collaborated with engineering, design, and marketing to achieve a 15% increase in MRR."""
}

# Generate the PDFs
print("Generating ATS-friendly PDFs...")
for filename, content in resumes.items():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    pdf.multi_cell(0, 6, content.encode('latin-1', 'replace').decode('latin-1'))
    pdf.output(filename)
    print(f"✅ Created {filename}")

print("Done! You can now upload these to your Streamlit app.")