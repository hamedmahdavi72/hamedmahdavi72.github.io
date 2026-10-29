# Shared content for all prototype directions. Edit here, then run build.py.

NAME = "Hamed Mahdavi"
TAGLINE = "LLM reasoning, post-training, and the data that drives them"
EMAIL = "hmm5834@psu.edu"
AFFIL = "Pennsylvania State University, State College, PA"
CV = "CV.pdf"

# (label, url, lettermark, secondary line)
LINKS = [
    ("Google Scholar", "https://scholar.google.com/citations?user=Ld-BcToAAAAJ", "GS", "publications and citations"),
    ("GitHub", "https://github.com/hamedmahdavi72", "GH", "@hamedmahdavi72"),
    ("LinkedIn", "https://www.linkedin.com/in/hamed-mahdavi-a95480103/", "in", "hamed-mahdavi"),
    ("Twitter", "https://twitter.com/hamedmahdavi93", "X", "@hamedmahdavi93"),
]

BIO = [
    "I am a Ph.D. candidate in Computer Science and Engineering at Pennsylvania State University, advised by "
    "Prof. Vasant Honavar, graduating in November 2026. My research is on reasoning in large language models. "
    "I build agentic workflows and evaluation harnesses that find where models fail, generate targeted synthetic "
    "data to fix those failures, and feed it back through SFT, RL, and pretraining.",
    "Most recently I was a Research Scientist Intern at a stealth AI startup in New York, "
    "training reward models for creative judgment. Before that I collaborated with Google's Gemini Data team on the "
    "<a href=\"https://deepmind.google/discover/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/\">Gemini IMO 2025</a> "
    "project, and my work on LLMs for mathematics is supported by an unrestricted research gift from Google.",
    "I am on the job market for research scientist roles starting late 2026, with a focus on LLM post-training, "
    "reasoning, and data.",
]

LOOP = [
    ("Evaluate", "Focused evals and failure analysis locate where a model breaks."),
    ("Generate", "Multi-step agents produce targeted, verifiable data for those failures."),
    ("Train", "Data goes where it helps most: SFT, RLHF, RLVR, or pretraining."),
    ("Benchmark", "Re-measure, keep what moved, and close the loop."),
]

NEWS = [
    ("Oct 2026", "<em>Splicing Hints into Reasoning Traces</em> is on <a href=\"https://arxiv.org/abs/2610.13996\">arXiv</a> and under review at ICLR 2027."),
    ("Aug 2026", "Wrapped up a six-month Research Scientist internship at a stealth AI startup in New York."),
    ("Mar 2026", "Joined a stealth AI startup in New York to work on reward models for creative judgment."),
    ("Oct 2025", "<em>RefGrader</em> and <em>CombiGraph-Vis</em> accepted to the Math-AI Workshop at NeurIPS 2025."),
    ("Jul 2025", "Collaborated with Google's Gemini Data team on the IMO 2025 gold medal effort."),
    ("May 2025", "Received a $100k unrestricted research gift from Google."),
    ("Apr 2025", "<em>Brains vs. Bytes</em> accepted to COLM 2025."),
]

# (title, org, location, dates, bullets, link)
EXPERIENCE = [
    ("Research Scientist Intern", "Stealth AI Startup", "New York, NY", "Mar 2026 – Aug 2026", [
        "Developed agentic workflows and evaluation harnesses for open-ended creative content generation, with a focus on generating synthetic reasoning data for creativity.",
        "Built pipelines that transform agentic workflows into training data, studying the interaction between mid-training and post-training for creative reasoning capabilities.",
        "Trained reasoning and non-reasoning reward models for creative judgment and led data curation for reward modeling in the creative judgment domain.",
    ], None),
    ("Collaborator, Gemini IMO 2025 Project", "Google", "New York, NY", "Summer 2025", [
        "Provided high-quality verifiable data and evaluations to the Gemini Data team under the supervision of Dr. Vahab Mirrokni, resulting in a gold medal at the International Mathematical Olympiad (IMO).",
    ], "https://deepmind.google/discover/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/"),
    ("Research Assistant", "Pennsylvania State University", "State College, PA", "Jan 2022 – Present", [
        "Design agentic workflows for math problem solving and high-quality mathematical data generation; build and run evaluation harnesses for contest-level math (benchmarks, metrics, ablations, failure analysis).",
    ], None),
    ("Data Scientist Intern", "Arconic Technology Center", "New Kensington, PA", "Jun 2023 – Aug 2023", [
        "Worked in the Fabrication Technology group under the supervision of Martin Marinack; tackled several data-driven optimization problems to improve Arconic's fabrication processes (welding, rolling, and casting).",
    ], None),
    ("Research Intern", "Max Planck Institute for Software Systems", "Saarbrücken, Germany", "Aug 2018 – Jan 2019", [
        "Worked on fundamental aspects of reinforcement learning, focusing on multi-agent, adversarial, and human-centered reinforcement learning.",
        "Studied how to design an AI agent that can robustly cooperate with agents of unknown types encountered only after deployment.",
    ], None),
    ("Software Engineering Intern", "Faragostar", "Tehran", "Jul 2017 – Sep 2017", [
        "Developed a compression algorithm that allowed Faragostar to retain its official documents while minimizing storage requirements.",
        "Configured infrastructure for Elasticsearch, enabling more efficient and complex searches than the previous SQL-based search tool.",
    ], None),
    ("Mathematical Olympiad Teacher", "Allameh Helli High School", "Tehran", "Oct 2012 – Apr 2013", [
        "Taught number theory to academically gifted students.",
    ], None),
]

# (title, authors, venue, year, links{label:url}, topics)
PUBS = [
    ("Splicing Hints into Reasoning Traces: Distillation Beyond What the Demonstrator Can Solve",
     "H. Mahdavi, P. Mahdavinia, M. Farhadi, V. Honavar", "Submitted to ICLR", "2027",
     {"arXiv": "https://arxiv.org/abs/2610.13996"}, ["Reasoning", "Post-training"]),
    ("RefGrader: Automated Grading of Mathematical Competition Proofs using Agentic Workflows",
     "H. Mahdavi, A. Hashemi, M. Daliri, P. Mohammadipour, A. Farhadi, S. Malek, Y. Yazdanifard, N. Mireshghallah, A. Khasahmadi, V. Honavar",
     "Math-AI Workshop, NeurIPS", "2025", {"arXiv": "https://arxiv.org/abs/2510.09021"}, ["Reasoning", "Evaluation"]),
    ("CombiGraph-Vis: A Multimodal Olympiad Benchmark for Discrete Mathematical Reasoning",
     "H. Mahdavi, A. Hashemi, M. Daliri, P. Mohammadipour, A. Farhadi, S. Malek, Y. Yazdanifard, A. Khasahmadi, V. Honavar",
     "Math-AI Workshop, NeurIPS", "2025",
     {"arXiv": "https://arxiv.org/abs/2510.27094", "Dataset": "https://huggingface.co/datasets/combviz/inoi"}, ["Reasoning", "Evaluation"]),
    ("Harnessing Optimization Dynamics for Curvature-Informed Model Merging",
     "P. Mahdavinia, H. Mahdavi, N. Mireshghallah, M. Mahdavi", "Preprint", "2025",
     {"arXiv": "https://arxiv.org/abs/2509.11167"}, ["Post-training"]),
    ("Brains vs. Bytes: Evaluating LLM Proficiency in Olympiad Mathematics",
     "H. Mahdavi, A. Hashemi, M. Daliri, P. Mohammadipour, A. Farhadi, S. Malek, Y. Yazdanifard, A. Khasahmadi, V. Honavar",
     "COLM", "2025", {"arXiv": "https://arxiv.org/abs/2504.01995"}, ["Reasoning", "Evaluation"]),
    ("Beyond Training Data: How Elemental Features Enhance ML-Based Formation Energy Predictions",
     "H. Mahdavi, V. Honavar, D. Morgan", "Digital Discovery", "2025",
     {"Paper": "https://doi.org/10.1039/D5DD00182J"}, ["Materials"]),
    ("Towards Deployment of Robust Cooperative AI Agents: An Algorithmic Framework for Learning Adaptive Policies",
     "A. Ghosh, S. Tschiatschek, H. Mahdavi, A. Singla", "AAMAS", "2020",
     {"arXiv": "https://arxiv.org/abs/1910.02330"}, ["Reinforcement Learning"]),
]

EDUCATION = [
    ("Ph.D. in Computer Science and Engineering", "Pennsylvania State University", "Jan 2022 – Nov 2026 (expected)",
     "Advisor: Prof. Vasant Honavar · Thesis: Solving Contest-Level Math Problems Using LLMs"),
    ("M.Sc. in Artificial Intelligence", "Sharif University of Technology", "Sep 2017 – Dec 2020",
     "Advisor: Prof. Hamid Beygi · Thesis: Approximate Inference in Probabilistic Network Models"),
    ("B.Sc. in Computer Engineering", "Sharif University of Technology", "Sep 2012 – Sep 2017",
     "Advisor: Prof. Hossein Sameti · Thesis: A Survey on Speech Enhancement Algorithms"),
]

HONORS = [
    ("$100k Unrestricted Research Gift from Google", "May 2025",
     "Awarded to support research on enhancing LLMs for mathematics through synthetic data generation and agentic workflows."),
    ("Top National Rankings in M.Sc. Entrance Exam", "Jun 2017",
     "Placed 5th (AI), 2nd (Networks and Security), and 4th (IT) nationwide."),
    ("Ranked 217th in National University Entrance Exam", "Jun 2012",
     "Top 0.1% among 260,000+ examinees nationwide."),
    ("Silver Medal, 29th National Mathematical Olympiad", "Sep 2011",
     "Selected as one of 40 participants from 100,000+ candidates."),
]

INTERESTS = [
    "LLMs for math problem solving",
    "Agentic workflows for synthetic data generation",
    "Reasoning in LLMs",
    "Post-training, reward modeling, and LLM-as-a-judge",
    "Reinforcement learning",
    "Optimization in machine learning",
]

OUTSIDE = ("Outside research I play tennis and badminton, which I have done since I was nine, "
           "and guitar, acoustic and electric, mostly classic rock.")
