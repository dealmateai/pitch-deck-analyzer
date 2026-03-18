"""
Enhanced Synthetic Data Generator
Creates 100 realistic startup records (50 positive YC + 50 negative non-YC)
Includes founder work experience, previous companies, and education
"""

import pandas as pd
from typing import List, Dict
from utils.logger import log

class SyntheticDataGenerator:
    """Generate realistic synthetic startup data with comprehensive founder backgrounds."""
    
    # ===== POSITIVE DATA (YC Companies - Label: 1) =====
    YC_COMPANIES_SYNTHETIC = [
        {
            "name": "Airbnb",
            "description": "Book accommodations around the world. We connect people to unique travel experiences at any price point in more than 33,000 cities and 192 countries. Our mission is to create a world where anyone can belong anywhere.",
            "industry": "Travel Tech",
            "founded_year": 2008,
            "batch": "Winter 2009",
            "status": "Public",
            "team_size": 6132,
            "location": "San Francisco, CA",
            "founders": ["Brian Chesky", "Nathan Blecharczyk", "Joe Gebbia"],
            "founder_experience": {
                "Brian Chesky": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "RISD", "position": "Student", "years": "2003-2007"}
                    ],
                    "education": "Rhode Island School of Design (BFA Industrial Design)",
                    "technical": False,
                },
                "Nathan Blecharczyk": {
                    "roles": ["Founder/CTO"],
                    "previous_companies": [
                        {"name": "Harvard", "position": "Student", "years": "2003-2007"},
                        {"name": "Various Startups", "position": "Software Engineer", "years": "2007-2008"}
                    ],
                    "education": "Harvard University (BS Computer Science)",
                    "technical": True,
                },
                "Joe Gebbia": {
                    "roles": ["Founder/Product"],
                    "previous_companies": [
                        {"name": "RISD", "position": "Student", "years": "2003-2007"}
                    ],
                    "education": "Rhode Island School of Design (BFA Industrial Design)",
                    "technical": False,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Stripe",
            "description": "Online payment processing platform. We enable businesses of all sizes to accept payments and move money globally. Stripe is the backbone of the internet economy, processing hundreds of billions in transactions annually.",
            "industry": "FinTech",
            "founded_year": 2010,
            "batch": "Summer 2010",
            "status": "Private",
            "team_size": 3200,
            "location": "San Francisco, CA",
            "founders": ["Patrick Collison", "John Collison"],
            "founder_experience": {
                "Patrick Collison": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "MIT", "position": "Student", "years": "2007-2010"},
                        {"name": "Auctomatic", "position": "CTO", "years": "2008-2010"}
                    ],
                    "education": "MIT (BS Computer Science)",
                    "technical": True,
                },
                "John Collison": {
                    "roles": ["Founder/President"],
                    "previous_companies": [
                        {"name": "University of Limerick", "position": "Student", "years": "2008-2011"},
                        {"name": "Auctomatic", "position": "Software Engineer", "years": "2009-2010"}
                    ],
                    "education": "University of Limerick (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Dropbox",
            "description": "Cloud storage and file synchronization service. We help millions of people store, sync, and share files securely. Our mission is to unlock human potential by designing a more enlightened way of working.",
            "industry": "Cloud Storage",
            "founded_year": 2008,
            "batch": "Summer 2007",
            "status": "Public",
            "team_size": 2500,
            "location": "San Francisco, CA",
            "founders": ["Drew Houston", "Arash Ferdowski"],
            "founder_experience": {
                "Drew Houston": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "MIT", "position": "Student", "years": "2001-2005"},
                        {"name": "Google", "position": "Software Engineer", "years": "2006-2008"}
                    ],
                    "education": "MIT (BS Computer Science)",
                    "technical": True,
                },
                "Arash Ferdowski": {
                    "roles": ["Founder/VP Product"],
                    "previous_companies": [
                        {"name": "San Jose State", "position": "Student", "years": "2001-2006"},
                        {"name": "Google", "position": "Software Engineer", "years": "2006-2008"}
                    ],
                    "education": "San Jose State University (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Airbnb Clone - TravelStay",
            "description": "Next generation accommodation marketplace connecting travelers with unique properties. We are disrupting the $1 trillion travel industry with AI-powered personalization and seamless booking experience.",
            "industry": "Travel Tech",
            "founded_year": 2022,
            "batch": "Winter 2023",
            "status": "Private",
            "team_size": 85,
            "location": "San Francisco, CA",
            "founders": ["Sarah Chen", "Michael Park"],
            "founder_experience": {
                "Sarah Chen": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Stanford", "position": "Student", "years": "2016-2020"},
                        {"name": "Airbnb", "position": "Product Manager", "years": "2020-2022"}
                    ],
                    "education": "Stanford University (BS Computer Science)",
                    "technical": True,
                },
                "Michael Park": {
                    "roles": ["Founder/CTO"],
                    "previous_companies": [
                        {"name": "UC Berkeley", "position": "Student", "years": "2016-2020"},
                        {"name": "Google", "position": "Software Engineer", "years": "2020-2022"}
                    ],
                    "education": "UC Berkeley (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "DoorDash",
            "description": "Restaurant delivery platform. We are building the delivery infrastructure for commerce. Through DoorDash, people get the food they love from their favorite local restaurants.",
            "industry": "E-commerce",
            "founded_year": 2013,
            "batch": "Summer 2013",
            "status": "Public",
            "team_size": 4500,
            "location": "San Francisco, CA",
            "founders": ["Tony Xu", "Stanley Tang", "Evan Moore"],
            "founder_experience": {
                "Tony Xu": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Stanford", "position": "Student", "years": "2007-2011"},
                        {"name": "McKinsey", "position": "Analyst", "years": "2011-2013"}
                    ],
                    "education": "Stanford University (BS Computer Science)",
                    "technical": True,
                },
                "Stanley Tang": {
                    "roles": ["Founder/VP Product"],
                    "previous_companies": [
                        {"name": "Stanford", "position": "Student", "years": "2007-2011"},
                        {"name": "Google", "position": "Software Engineer", "years": "2011-2013"}
                    ],
                    "education": "Stanford University (BS Computer Science)",
                    "technical": True,
                },
                "Evan Moore": {
                    "roles": ["Founder/COO"],
                    "previous_companies": [
                        {"name": "Stanford", "position": "Student", "years": "2007-2012"},
                        {"name": "Amazon", "position": "Associate", "years": "2012-2013"}
                    ],
                    "education": "Stanford University (BS Management Science)",
                    "technical": False,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Figma",
            "description": "Collaborative design tool. Figma is the place where design happens. We are building the first browser-based design tool with real-time collaboration for teams to design better products together.",
            "industry": "Design Tech",
            "founded_year": 2016,
            "batch": "N/A",
            "status": "Private",
            "team_size": 1200,
            "location": "San Francisco, CA",
            "founders": ["Dylan Field", "Evan Wallace"],
            "founder_experience": {
                "Dylan Field": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Brown", "position": "Student", "years": "2012-2016"},
                        {"name": "Intercom", "position": "Product Engineer", "years": "2015-2016"}
                    ],
                    "education": "Brown University (BS Computer Science)",
                    "technical": True,
                },
                "Evan Wallace": {
                    "roles": ["Founder/VP Design"],
                    "previous_companies": [
                        {"name": "Dartmouth", "position": "Student", "years": "2010-2014"}
                    ],
                    "education": "Dartmouth College (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Slack",
            "description": "Business communication platform. Slack transforms how people work together. We bring all your communication together in one place to make teams more productive and connected.",
            "industry": "SaaS",
            "founded_year": 2011,
            "batch": "N/A",
            "status": "Public",
            "team_size": 2300,
            "location": "San Francisco, CA",
            "founders": ["Stewart Butterfield"],
            "founder_experience": {
                "Stewart Butterfield": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "University of Victoria", "position": "Student", "years": "1995-1999"},
                        {"name": "Flickr", "position": "Co-founder/CEO", "years": "2004-2006"},
                        {"name": "Yahoo", "position": "Executive", "years": "2006-2008"}
                    ],
                    "education": "University of Victoria (BA Philosophy)",
                    "technical": False,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Twilio",
            "description": "Cloud communications platform. We enable developers to build communications into their applications. Twilio powers the future of business communications for millions of users worldwide.",
            "industry": "SaaS",
            "founded_year": 2008,
            "batch": "Summer 2008",
            "status": "Public",
            "team_size": 1800,
            "location": "San Francisco, CA",
            "founders": ["Jeff Lawson"],
            "founder_experience": {
                "Jeff Lawson": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "University of Nevada", "position": "Student", "years": "2002-2006"},
                        {"name": "Amazon", "position": "Software Engineer", "years": "2006-2008"}
                    ],
                    "education": "University of Nevada, Reno (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Notion",
            "description": "All-in-one workspace. Notion is where work happens. We are building the all-in-one workspace for notes, tasks, wikis, and databases to help teams work more effectively together.",
            "industry": "Productivity",
            "founded_year": 2016,
            "batch": "N/A",
            "status": "Private",
            "team_size": 650,
            "location": "San Francisco, CA",
            "founders": ["Ivan Zhao"],
            "founder_experience": {
                "Ivan Zhao": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "University of Toronto", "position": "Student", "years": "2011-2015"},
                        {"name": "Dropbox", "position": "Software Engineer", "years": "2015-2016"}
                    ],
                    "education": "University of Toronto (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Instacart",
            "description": "Grocery delivery service. We connect customers with restaurant and food delivery services. Our mission is to empower local economies by enabling people to get what they need.",
            "industry": "E-commerce",
            "founded_year": 2012,
            "batch": "Summer 2012",
            "status": "Private",
            "team_size": 3000,
            "location": "San Francisco, CA",
            "founders": ["Apoorva Mehta"],
            "founder_experience": {
                "Apoorva Mehta": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "UC Berkeley", "position": "Student", "years": "2004-2008"},
                        {"name": "Amazon", "position": "Software Engineer", "years": "2008-2010"},
                        {"name": "Flipkart", "position": "Senior Engineer", "years": "2010-2012"}
                    ],
                    "education": "UC Berkeley (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Uber",
            "description": "Ride-sharing and delivery platform. We reimagine the way people and things move around cities. Uber is the platform that makes transportation accessible.",
            "industry": "Transportation",
            "founded_year": 2009,
            "batch": "N/A",
            "status": "Public",
            "team_size": 6500,
            "location": "San Francisco, CA",
            "founders": ["Travis Kalanick", "Garrett Camp"],
            "founder_experience": {
                "Travis Kalanick": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "UCLA", "position": "Student", "years": "2000-2002"},
                        {"name": "Red Swoosh", "position": "Co-founder/CEO", "years": "2002-2008"}
                    ],
                    "education": "UCLA (BS Computer Science)",
                    "technical": True,
                },
                "Garrett Camp": {
                    "roles": ["Founder/CTO"],
                    "previous_companies": [
                        {"name": "University of Waterloo", "position": "Student", "years": "2003-2007"},
                        {"name": "StumbleUpon", "position": "Co-founder/CTO", "years": "2007-2012"}
                    ],
                    "education": "University of Waterloo (BS Software Engineering)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Canva",
            "description": "Design platform for everyone. Canva empowers the world to design. We are democratizing design by making professional design accessible to everyone without special training.",
            "industry": "Design Tech",
            "founded_year": 2013,
            "batch": "N/A",
            "status": "Private",
            "team_size": 800,
            "location": "Sydney, Australia",
            "founders": ["Melanie Perkins"],
            "founder_experience": {
                "Melanie Perkins": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "UNSW Sydney", "position": "Student", "years": "2009-2012"},
                        {"name": "Fusion Books", "position": "Founder/CEO", "years": "2011-2013"}
                    ],
                    "education": "UNSW Sydney (BS Commerce)",
                    "technical": False,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "OpenAI",
            "description": "AI research and deployment company. We are conducting research to ensure artificial general intelligence benefits all of humanity. OpenAI develops safe and beneficial AI systems.",
            "industry": "AI/ML",
            "founded_year": 2015,
            "batch": "N/A",
            "status": "Private",
            "team_size": 900,
            "location": "San Francisco, CA",
            "founders": ["Sam Altman", "Elon Musk"],
            "founder_experience": {
                "Sam Altman": {
                    "roles": ["CEO"],
                    "previous_companies": [
                        {"name": "Stanford", "position": "Student", "years": "2003-2005"},
                        {"name": "Loopt", "position": "CEO", "years": "2005-2013"},
                        {"name": "Y Combinator", "position": "President", "years": "2014-2019"}
                    ],
                    "education": "Stanford University (BS Computer Science)",
                    "technical": True,
                },
                "Elon Musk": {
                    "roles": ["Co-founder"],
                    "previous_companies": [
                        {"name": "University of Pennsylvania", "position": "Student", "years": "1992-1995"},
                        {"name": "Zip2", "position": "Co-founder/CEO", "years": "1995-1999"},
                        {"name": "PayPal", "position": "Co-founder/CEO", "years": "1999-2002"},
                        {"name": "SpaceX", "position": "CEO", "years": "2002-present"}
                    ],
                    "education": "University of Pennsylvania (BS Physics & Economics)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Coursera",
            "description": "Online learning platform. We aim to provide universal access to world-class education. Coursera partners with universities and companies to offer courses on almost every subject.",
            "industry": "EdTech",
            "founded_year": 2012,
            "batch": "N/A",
            "status": "Public",
            "team_size": 1500,
            "location": "Mountain View, CA",
            "founders": ["Andrew Ng", "Daphne Koller"],
            "founder_experience": {
                "Andrew Ng": {
                    "roles": ["Co-founder/Chairman"],
                    "previous_companies": [
                        {"name": "Carnegie Mellon", "position": "Student", "years": "1997-2000"},
                        {"name": "Stanford", "position": "Professor", "years": "2002-2011"},
                        {"name": "Google", "position": "VP Research", "years": "2011-2014"}
                    ],
                    "education": "Carnegie Mellon University (BS CS), UC Berkeley (PhD CS)",
                    "technical": True,
                },
                "Daphne Koller": {
                    "roles": ["Co-founder/President"],
                    "previous_companies": [
                        {"name": "Hebrew University", "position": "Student", "years": "1990-1994"},
                        {"name": "Stanford", "position": "Professor", "years": "1998-2016"}
                    ],
                    "education": "Hebrew University (BS CS), Stanford University (PhD CS)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Palantir",
            "description": "Big data analytics platform. We transform data into actionable intelligence. Palantir's software is used by the world's most important institutions to uncover the truth in data.",
            "industry": "Data Analytics",
            "founded_year": 2003,
            "batch": "N/A",
            "status": "Public",
            "team_size": 3800,
            "location": "Denver, CO",
            "founders": ["Peter Thiel", "Alex Karp"],
            "founder_experience": {
                "Peter Thiel": {
                    "roles": ["Co-founder"],
                    "previous_companies": [
                        {"name": "Stanford", "position": "Student", "years": "1989-1992"},
                        {"name": "PayPal", "position": "CEO", "years": "1998-2002"}
                    ],
                    "education": "Stanford University (BS Philosophy & Economics)",
                    "technical": False,
                },
                "Alex Karp": {
                    "roles": ["CEO"],
                    "previous_companies": [
                        {"name": "University of Pennsylvania", "position": "Student", "years": "1990-1993"},
                        {"name": "Stanford", "position": "Postdoc", "years": "1995-2001"}
                    ],
                    "education": "University of Pennsylvania (BA Philosophy), Stanford (PhD Philosophy)",
                    "technical": False,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Datadog",
            "description": "Monitoring and analytics platform. We help organizations optimize their cloud infrastructure. Datadog monitors applications, infrastructure, and user experience across the entire stack.",
            "industry": "DevOps",
            "founded_year": 2010,
            "batch": "Summer 2010",
            "status": "Public",
            "team_size": 2200,
            "location": "New York, NY",
            "founders": ["Olivier Pomel", "Alexis Lê-Quôc"],
            "founder_experience": {
                "Olivier Pomel": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Polytechnique", "position": "Student", "years": "2001-2004"},
                        {"name": "Google", "position": "Software Engineer", "years": "2005-2010"}
                    ],
                    "education": "Polytechnique (Engineering Degree)",
                    "technical": True,
                },
                "Alexis Lê-Quôc": {
                    "roles": ["Co-founder"],
                    "previous_companies": [
                        {"name": "Polytechnique", "position": "Student", "years": "2001-2004"},
                        {"name": "Google", "position": "Software Engineer", "years": "2005-2010"}
                    ],
                    "education": "Polytechnique (Engineering Degree)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Zapier",
            "description": "Workflow automation platform. We connect your apps and automate workflows. Zapier helps teams accomplish more by automating repetitive tasks across your favorite apps.",
            "industry": "SaaS",
            "founded_year": 2011,
            "batch": "Summer 2011",
            "status": "Private",
            "team_size": 450,
            "location": "San Francisco, CA",
            "founders": ["Wade Foster"],
            "founder_experience": {
                "Wade Foster": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "University of Iowa", "position": "Student", "years": "2005-2009"},
                        {"name": "Web Dev Shop", "position": "Founder/Developer", "years": "2009-2011"}
                    ],
                    "education": "University of Iowa (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "GitLab",
            "description": "DevOps platform. We are the DevOps platform delivering value throughout the software development and operations lifecycle. GitLab integrates all the tools needed for software development.",
            "industry": "DevOps",
            "founded_year": 2013,
            "batch": "N/A",
            "status": "Public",
            "team_size": 1800,
            "location": "San Francisco, CA",
            "founders": ["Sid Sijbrandij"],
            "founder_experience": {
                "Sid Sijbrandij": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "University of Amsterdam", "position": "Student", "years": "2005-2010"},
                        {"name": "Parallo", "position": "Founder/Developer", "years": "2010-2013"}
                    ],
                    "education": "University of Amsterdam (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Loom",
            "description": "Video messaging platform. Loom is the easiest way to communicate using instant video messages. Record your screen, share instantly, and save time on meetings.",
            "industry": "Productivity",
            "founded_year": 2016,
            "batch": "Winter 2016",
            "status": "Private",
            "team_size": 250,
            "location": "San Francisco, CA",
            "founders": ["Joe Thomas"],
            "founder_experience": {
                "Joe Thomas": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Stanford", "position": "Student", "years": "2010-2014"},
                        {"name": "Google", "position": "Product Manager", "years": "2014-2016"}
                    ],
                    "education": "Stanford University (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Guidepoint",
            "description": "Expert network platform. We connect professionals with experts for insights. Guidepoint enables companies to tap into expert knowledge for better decision making.",
            "industry": "B2B SaaS",
            "founded_year": 2012,
            "batch": "Winter 2012",
            "status": "Private",
            "team_size": 800,
            "location": "New York, NY",
            "founders": ["Shayle Compton"],
            "founder_experience": {
                "Shayle Compton": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Duke", "position": "Student", "years": "2005-2009"},
                        {"name": "Bain & Company", "position": "Consultant", "years": "2009-2012"}
                    ],
                    "education": "Duke University (BS Economics)",
                    "technical": False,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Segment",
            "description": "Customer data platform. We collect, clean, and activate customer data. Segment is the leading Customer Data Platform helping businesses make data-driven decisions.",
            "industry": "Data Analytics",
            "founded_year": 2011,
            "batch": "Summer 2011",
            "status": "Public",
            "team_size": 1000,
            "location": "San Francisco, CA",
            "founders": ["Peter Reinhardt"],
            "founder_experience": {
                "Peter Reinhardt": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "UC Berkeley", "position": "Student", "years": "2006-2010"},
                        {"name": "Google", "position": "Software Engineer", "years": "2010-2011"}
                    ],
                    "education": "UC Berkeley (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Airtable",
            "description": "Low-code database platform. Airtable combines the simplicity of a spreadsheet with the power of a database. We are democratizing software creation for millions of users.",
            "industry": "SaaS",
            "founded_year": 2012,
            "batch": "Summer 2012",
            "status": "Private",
            "team_size": 800,
            "location": "San Francisco, CA",
            "founders": ["Howie Liu"],
            "founder_experience": {
                "Howie Liu": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "MIT", "position": "Student", "years": "2005-2009"},
                        {"name": "Google", "position": "Software Engineer", "years": "2009-2012"}
                    ],
                    "education": "MIT (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Amplitude",
            "description": "Product analytics platform. We help companies build better products with data-driven insights. Amplitude enables digital leaders to understand user behavior and drive growth.",
            "industry": "Analytics",
            "founded_year": 2012,
            "batch": "Summer 2012",
            "status": "Public",
            "team_size": 900,
            "location": "San Francisco, CA",
            "founders": ["Curtis Lee", "Spencer Kimball"],
            "founder_experience": {
                "Curtis Lee": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Harvard", "position": "Student", "years": "2008-2012"},
                        {"name": "Zynga", "position": "Data Analyst", "years": "2012-2014"}
                    ],
                    "education": "Harvard University (BS Applied Mathematics)",
                    "technical": True,
                },
                "Spencer Kimball": {
                    "roles": ["Co-founder/VP Engineering"],
                    "previous_companies": [
                        {"name": "UC Berkeley", "position": "Student", "years": "2007-2011"},
                        {"name": "Google", "position": "Software Engineer", "years": "2011-2012"}
                    ],
                    "education": "UC Berkeley (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Webpack AI",
            "description": "AI-powered developer tools. We use AI to help developers code faster and better. Our tools integrate seamlessly into existing development workflows.",
            "industry": "Developer Tools",
            "founded_year": 2023,
            "batch": "Winter 2023",
            "status": "Private",
            "team_size": 45,
            "location": "San Francisco, CA",
            "founders": ["Alex Kumar", "Priya Singh"],
            "founder_experience": {
                "Alex Kumar": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Stanford", "position": "Student", "years": "2017-2021"},
                        {"name": "Meta", "position": "Software Engineer", "years": "2021-2023"}
                    ],
                    "education": "Stanford University (BS Computer Science)",
                    "technical": True,
                },
                "Priya Singh": {
                    "roles": ["Founder/CTO"],
                    "previous_companies": [
                        {"name": "IIT Delhi", "position": "Student", "years": "2017-2021"},
                        {"name": "Google", "position": "Software Engineer", "years": "2021-2023"}
                    ],
                    "education": "IIT Delhi (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "CloudFlare",
            "description": "Web performance and security company. We make the internet faster and safer. CloudFlare protects and accelerates web applications for millions of users worldwide.",
            "industry": "Infrastructure",
            "founded_year": 2009,
            "batch": "Summer 2010",
            "status": "Public",
            "team_size": 2500,
            "location": "San Francisco, CA",
            "founders": ["Matthew Prince"],
            "founder_experience": {
                "Matthew Prince": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Harvard", "position": "Student", "years": "2001-2005"},
                        {"name": "Unspun", "position": "CTO", "years": "2006-2009"}
                    ],
                    "education": "Harvard University (BA Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Retool",
            "description": "Low-code internal tools platform. We help organizations build internal tools 10x faster. Retool is the fastest way to build business software.",
            "industry": "Developer Tools",
            "founded_year": 2019,
            "batch": "Winter 2019",
            "status": "Private",
            "team_size": 200,
            "location": "San Francisco, CA",
            "founders": ["David Hsu"],
            "founder_experience": {
                "David Hsu": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Yale", "position": "Student", "years": "2012-2016"},
                        {"name": "Oracle", "position": "Software Engineer", "years": "2016-2019"}
                    ],
                    "education": "Yale University (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Superhuman",
            "description": "High-speed email client. We revolutionize how people work with email. Superhuman helps professionals reclaim time by making email faster and more efficient.",
            "industry": "Productivity",
            "founded_year": 2015,
            "batch": "Winter 2015",
            "status": "Private",
            "team_size": 150,
            "location": "San Francisco, CA",
            "founders": ["Rahul Vohra"],
            "founder_experience": {
                "Rahul Vohra": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Cornell", "position": "Student", "years": "2008-2012"},
                        {"name": "Superhuman Labs", "position": "Founder/CEO", "years": "2015-present"}
                    ],
                    "education": "Cornell University (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Craft.co",
            "description": "B2B database platform. We provide the most accurate and complete B2B data. Craft is the leading platform for finding and understanding companies.",
            "industry": "B2B Data",
            "founded_year": 2017,
            "batch": "Summer 2017",
            "status": "Private",
            "team_size": 400,
            "location": "San Francisco, CA",
            "founders": ["Micah Alcorn"],
            "founder_experience": {
                "Micah Alcorn": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Brigham Young", "position": "Student", "years": "2011-2016"},
                        {"name": "LinkedIn", "position": "Data Analyst", "years": "2016-2017"}
                    ],
                    "education": "Brigham Young University (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "Zapier Clone - FlowMate",
            "description": "Automation workflow builder connecting business applications. We simplify business processes through intelligent automation and seamless integrations.",
            "industry": "SaaS",
            "founded_year": 2023,
            "batch": "Summer 2023",
            "status": "Private",
            "team_size": 65,
            "location": "Austin, TX",
            "founders": ["John Martinez", "Lisa Chen"],
            "founder_experience": {
                "John Martinez": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "University of Texas", "position": "Student", "years": "2016-2020"},
                        {"name": "Microsoft", "position": "Software Engineer", "years": "2020-2023"}
                    ],
                    "education": "University of Texas at Austin (BS Computer Science)",
                    "technical": True,
                },
                "Lisa Chen": {
                    "roles": ["Founder/CTO"],
                    "previous_companies": [
                        {"name": "UT Austin", "position": "Student", "years": "2016-2020"},
                        {"name": "Amazon", "position": "Software Engineer", "years": "2020-2023"}
                    ],
                    "education": "University of Texas at Austin (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "ByteDance AI Tools",
            "description": "AI-powered content creation suite. We democratize AI for content creators and businesses. Our tools help creators produce professional content effortlessly.",
            "industry": "AI/ML",
            "founded_year": 2022,
            "batch": "Spring 2023",
            "status": "Private",
            "team_size": 120,
            "location": "Beijing, China",
            "founders": ["Wei Song", "Alex Zhang"],
            "founder_experience": {
                "Wei Song": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Tsinghua University", "position": "Student", "years": "2015-2019"},
                        {"name": "ByteDance", "position": "AI Engineer", "years": "2019-2022"}
                    ],
                    "education": "Tsinghua University (BS Computer Science)",
                    "technical": True,
                },
                "Alex Zhang": {
                    "roles": ["Founder/CTO"],
                    "previous_companies": [
                        {"name": "Peking University", "position": "Student", "years": "2014-2018"},
                        {"name": "Google AI", "position": "Research Engineer", "years": "2018-2022"}
                    ],
                    "education": "Peking University (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "FinFlow Platform",
            "description": "Financial operations automation. We streamline financial workflows for growing companies. FinFlow reduces manual processes and improves financial accuracy.",
            "industry": "FinTech",
            "founded_year": 2022,
            "batch": "Winter 2022",
            "status": "Private",
            "team_size": 95,
            "location": "New York, NY",
            "founders": ["Michael Torres", "Emily Watson"],
            "founder_experience": {
                "Michael Torres": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "NYU", "position": "Student", "years": "2015-2019"},
                        {"name": "Goldman Sachs", "position": "Financial Analyst", "years": "2019-2022"}
                    ],
                    "education": "NYU (BS Finance)",
                    "technical": False,
                },
                "Emily Watson": {
                    "roles": ["Founder/CTO"],
                    "previous_companies": [
                        {"name": "MIT", "position": "Student", "years": "2015-2019"},
                        {"name": "JP Morgan", "position": "Software Engineer", "years": "2019-2022"}
                    ],
                    "education": "MIT (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "HRFlow Analytics",
            "description": "AI-powered HR analytics platform. We help organizations make better people decisions. Our platform provides insights into hiring, retention, and employee performance.",
            "industry": "HR Tech",
            "founded_year": 2020,
            "batch": "Summer 2020",
            "status": "Private",
            "team_size": 110,
            "location": "San Francisco, CA",
            "founders": ["Robert Chen"],
            "founder_experience": {
                "Robert Chen": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "UC Berkeley", "position": "Student", "years": "2012-2016"},
                        {"name": "Workday", "position": "Product Manager", "years": "2016-2020"}
                    ],
                    "education": "UC Berkeley (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "CloudSecure Pro",
            "description": "Cloud security platform for enterprises. We protect cloud infrastructure from threats. CloudSecure provides comprehensive security across AWS, Azure, and GCP.",
            "industry": "Cybersecurity",
            "founded_year": 2021,
            "batch": "Fall 2021",
            "status": "Private",
            "team_size": 140,
            "location": "San Jose, CA",
            "founders": ["David Patel", "Anita Sharma"],
            "founder_experience": {
                "David Patel": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Stanford", "position": "Student", "years": "2014-2018"},
                        {"name": "Palo Alto Networks", "position": "Security Engineer", "years": "2018-2021"}
                    ],
                    "education": "Stanford University (BS Computer Science)",
                    "technical": True,
                },
                "Anita Sharma": {
                    "roles": ["Founder/CTO"],
                    "previous_companies": [
                        {"name": "Carnegie Mellon", "position": "Student", "years": "2014-2018"},
                        {"name": "Microsoft", "position": "Security Engineer", "years": "2018-2021"}
                    ],
                    "education": "Carnegie Mellon University (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "MedAssist AI",
            "description": "AI diagnostics platform for healthcare. We help medical professionals make better diagnoses. Our AI analyzes medical imaging with high accuracy.",
            "industry": "HealthTech",
            "founded_year": 2021,
            "batch": "Winter 2021",
            "status": "Private",
            "team_size": 85,
            "location": "Boston, MA",
            "founders": ["Dr. James Lee"],
            "founder_experience": {
                "Dr. James Lee": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Harvard Medical School", "position": "Resident", "years": "2014-2018"},
                        {"name": "MIT", "position": "AI Researcher", "years": "2018-2021"}
                    ],
                    "education": "Stanford University (MD), MIT (MS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "EduConnect Pro",
            "description": "Online learning marketplace connecting students with tutors. We revolutionize education through personalized learning. EduConnect makes quality education accessible to all.",
            "industry": "EdTech",
            "founded_year": 2020,
            "batch": "Spring 2020",
            "status": "Private",
            "team_size": 200,
            "location": "San Francisco, CA",
            "founders": ["Sarah Johnson"],
            "founder_experience": {
                "Sarah Johnson": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Berkeley", "position": "Student", "years": "2014-2018"},
                        {"name": "Chegg", "position": "Product Manager", "years": "2018-2020"}
                    ],
                    "education": "UC Berkeley (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "LogiFlow",
            "description": "Supply chain optimization platform. We use AI to optimize logistics operations. LogiFlow helps companies reduce delivery costs and improve efficiency.",
            "industry": "Logistics",
            "founded_year": 2021,
            "batch": "Summer 2021",
            "status": "Private",
            "team_size": 180,
            "location": "Los Angeles, CA",
            "founders": ["Carlos Mendez"],
            "founder_experience": {
                "Carlos Mendez": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "UCLA", "position": "Student", "years": "2014-2018"},
                        {"name": "Amazon Logistics", "position": "Operations Manager", "years": "2018-2021"}
                    ],
                    "education": "UCLA (BS Operations Research)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "GreenEnergyHub",
            "description": "Renewable energy marketplace. We connect businesses with green energy solutions. GreenEnergyHub is accelerating the transition to sustainable energy.",
            "industry": "Clean Energy",
            "founded_year": 2019,
            "batch": "Summer 2019",
            "status": "Private",
            "team_size": 160,
            "location": "Boulder, CO",
            "founders": ["Tom Williams"],
            "founder_experience": {
                "Tom Williams": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Colorado University", "position": "Student", "years": "2012-2016"},
                        {"name": "NextEra Energy", "position": "Energy Analyst", "years": "2016-2019"}
                    ],
                    "education": "University of Colorado Boulder (BS Environmental Engineering)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "ResearchAI",
            "description": "AI research tool for academics. We accelerate scientific discovery through AI. ResearchAI helps researchers find and analyze papers efficiently.",
            "industry": "Research Tech",
            "founded_year": 2022,
            "batch": "Fall 2022",
            "status": "Private",
            "team_size": 75,
            "location": "Stanford, CA",
            "founders": ["Professor Alex Kumar"],
            "founder_experience": {
                "Professor Alex Kumar": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Stanford", "position": "Professor", "years": "2010-2022"},
                        {"name": "Google Research", "position": "Visiting Scholar", "years": "2015-2016"}
                    ],
                    "education": "Stanford University (PhD Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "PropertyTech AI",
            "description": "Real estate analytics platform. We help investors identify property opportunities. PropertyTech uses ML to predict market trends and property values.",
            "industry": "Real Estate",
            "founded_year": 2020,
            "batch": "Spring 2020",
            "status": "Private",
            "team_size": 130,
            "location": "San Francisco, CA",
            "founders": ["Victoria Lee"],
            "founder_experience": {
                "Victoria Lee": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "UC Berkeley", "position": "Student", "years": "2013-2017"},
                        {"name": "Zillow", "position": "Data Scientist", "years": "2017-2020"}
                    ],
                    "education": "UC Berkeley (BS Statistics & Economics)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "LawyerBot",
            "description": "Legal tech platform powered by AI. We make legal services accessible and affordable. LawyerBot provides automated contract review and legal assistance.",
            "industry": "Legal Tech",
            "founded_year": 2021,
            "batch": "Winter 2021",
            "status": "Private",
            "team_size": 95,
            "location": "New York, NY",
            "founders": ["Jennifer Rodriguez"],
            "founder_experience": {
                "Jennifer Rodriguez": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Harvard Law", "position": "Law Student", "years": "2015-2018"},
                        {"name": "WilmerHale", "position": "Associate", "years": "2018-2021"}
                    ],
                    "education": "Harvard Law School (JD)",
                    "technical": False,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "FarmTech Solutions",
            "description": "Agricultural technology platform. We help farmers optimize crop yields. FarmTech uses IoT and AI for precision agriculture.",
            "industry": "AgTech",
            "founded_year": 2020,
            "batch": "Summer 2020",
            "status": "Private",
            "team_size": 110,
            "location": "Ames, IA",
            "founders": ["David Zhang"],
            "founder_experience": {
                "David Zhang": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Iowa State", "position": "Student", "years": "2014-2018"},
                        {"name": "John Deere", "position": "Engineer", "years": "2018-2020"}
                    ],
                    "education": "Iowa State University (BS Agricultural Engineering)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "GameStudio Engine",
            "description": "Game development platform. We democratize game creation. GameStudio Engine helps creators build games without coding.",
            "industry": "Gaming",
            "founded_year": 2021,
            "batch": "Summer 2021",
            "status": "Private",
            "team_size": 180,
            "location": "Los Angeles, CA",
            "founders": ["Marcus Johnson"],
            "founder_experience": {
                "Marcus Johnson": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "USC", "position": "Student", "years": "2014-2018"},
                        {"name": "EA Games", "position": "Game Programmer", "years": "2018-2021"}
                    ],
                    "education": "USC (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
        {
            "name": "FashionAI",
            "description": "Fashion tech platform using AI for personalization. We revolutionize online shopping with virtual try-on and recommendations.",
            "industry": "Fashion Tech",
            "founded_year": 2022,
            "batch": "Spring 2022",
            "status": "Private",
            "team_size": 105,
            "location": "New York, NY",
            "founders": ["Natalie Scott"],
            "founder_experience": {
                "Natalie Scott": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "FIT", "position": "Student", "years": "2015-2019"},
                        {"name": "Stitch Fix", "position": "AI Stylist", "years": "2019-2022"}
                    ],
                    "education": "Fashion Institute of Technology (BS Fashion Design)",
                    "technical": False,
                }
            },
            "source": "YCombinator",
            "label": 1
        },
    ]
    
    # ===== NEGATIVE DATA (Non-YC Companies - Label: 0) =====
    NON_YC_COMPANIES_SYNTHETIC = [
        {
            "name": "LocalServices Pro",
            "description": "Small local service directory connecting customers with nearby service providers. Limited market reach and simple technology.",
            "industry": "Local Services",
            "founded_year": 2018,
            "batch": "N/A",
            "status": "Private",
            "team_size": 8,
            "location": "Austin, TX",
            "founders": ["Mike Johnson"],
            "founder_experience": {
                "Mike Johnson": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "University of Texas", "position": "Student", "years": "2014-2018"}
                    ],
                    "education": "University of Texas (BS Business)",
                    "technical": False,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "Community Garden App",
            "description": "Mobile app connecting urban gardeners. Niche market with limited scalability. Focuses on local community engagement only.",
            "industry": "Lifestyle",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 5,
            "location": "Portland, OR",
            "founders": ["Sarah Green"],
            "founder_experience": {
                "Sarah Green": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "Oregon State University (BS Environmental Science)",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Freelance Writer Hub",
            "description": "Platform connecting writers with clients. Highly fragmented market with many competitors. Minimal differentiation.",
            "industry": "Marketplace",
            "founded_year": 2017,
            "batch": "N/A",
            "status": "Private",
            "team_size": 12,
            "location": "Bangalore, India",
            "founders": ["Raj Patel"],
            "founder_experience": {
                "Raj Patel": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "IIT Bombay", "position": "Student", "years": "2013-2017"},
                        {"name": "Infosys", "position": "Junior Associate", "years": "2017-2018"}
                    ],
                    "education": "IIT Bombay (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "Pet Grooming Scheduler",
            "description": "Booking system for pet grooming salons. Limited to pet services niche. Low barrier to entry with strong competition.",
            "industry": "Pet Services",
            "founded_year": 2018,
            "batch": "N/A",
            "status": "Private",
            "team_size": 6,
            "location": "Denver, CO",
            "founders": ["Emma Wilson"],
            "founder_experience": {
                "Emma Wilson": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "Colorado State University (BS Business)",
                    "technical": False,
                }
            },
            "source": "Wellfound",
            "label": 0
        },
        {
            "name": "Personal Fitness Tracker",
            "description": "Mobile fitness app tracking workouts. Saturated market with established players like Strava and MyFitnessPal.",
            "industry": "Fitness",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 9,
            "location": "Los Angeles, CA",
            "founders": ["Jason Lee"],
            "founder_experience": {
                "Jason Lee": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "LA Fitness", "position": "Gym Trainer", "years": "2017-2019"}
                    ],
                    "education": "University of Southern California (BS Kinesiology)",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Local Restaurant Reviews",
            "description": "Restaurant review platform for a single city. Competes with Yelp and Google Reviews. Limited market size.",
            "industry": "Reviews",
            "founded_year": 2020,
            "batch": "N/A",
            "status": "Private",
            "team_size": 7,
            "location": "Seattle, WA",
            "founders": ["Tom Brown"],
            "founder_experience": {
                "Tom Brown": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "University of Washington (BS Business)",
                    "technical": False,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "DIY Home Improvement Store",
            "description": "Online store selling DIY tools and materials. Heavy competition from Home Depot and Lowe's. No clear differentiation.",
            "industry": "E-commerce",
            "founded_year": 2017,
            "batch": "N/A",
            "status": "Private",
            "team_size": 15,
            "location": "Atlanta, GA",
            "founders": ["Richard Davis"],
            "founder_experience": {
                "Richard Davis": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Home Depot", "position": "Store Manager", "years": "2015-2017"}
                    ],
                    "education": "Georgia Tech (BS Business)",
                    "technical": False,
                }
            },
            "source": "Wellfound",
            "label": 0
        },
        {
            "name": "Music Lesson Platform",
            "description": "Connect music teachers with students online. Highly fragmented with many small competitors. Limited differentiation.",
            "industry": "EdTech",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 8,
            "location": "Nashville, TN",
            "founders": ["Lucy Nelson"],
            "founder_experience": {
                "Lucy Nelson": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "Belmont University (BM Music Performance)",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Event Planning Assistant",
            "description": "Event planning software for small event planners. Niche market with limited growth potential. Outdated technology.",
            "industry": "Events",
            "founded_year": 2016,
            "batch": "N/A",
            "status": "Private",
            "team_size": 6,
            "location": "Las Vegas, NV",
            "founders": ["Patricia White"],
            "founder_experience": {
                "Patricia White": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "University of Nevada Las Vegas (BS Hospitality)",
                    "technical": False,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "Photography Portfolio Site",
            "description": "Portfolio website builder for photographers. Redundant market with Wix and Squarespace. Minimal innovation.",
            "industry": "SaaS",
            "founded_year": 2018,
            "batch": "N/A",
            "status": "Private",
            "team_size": 5,
            "location": "Portland, ME",
            "founders": ["Chris Anderson"],
            "founder_experience": {
                "Chris Anderson": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "Maine College of Art (BFA Photography)",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Craft Beer Marketplace",
            "description": "Local craft beer delivery service. Limited geographic expansion. High operating costs.",
            "industry": "E-commerce",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 10,
            "location": "Boulder, CO",
            "founders": ["Kevin Miller"],
            "founder_experience": {
                "Kevin Miller": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Local Brewery", "position": "Manager", "years": "2016-2019"}
                    ],
                    "education": "University of Colorado Boulder (BS Business)",
                    "technical": False,
                }
            },
            "source": "Wellfound",
            "label": 0
        },
        {
            "name": "Vintage Clothing Store",
            "description": "Online vintage clothing seller. Niche market with inconsistent supply. Difficult scalability.",
            "industry": "E-commerce",
            "founded_year": 2017,
            "batch": "N/A",
            "status": "Private",
            "team_size": 4,
            "location": "Portland, OR",
            "founders": ["Nina Martinez"],
            "founder_experience": {
                "Nina Martinez": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "Portland State University (BS Fashion)",
                    "technical": False,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "Corporate Gift Service",
            "description": "Custom corporate gift provider. B2B market but low margins. High customer acquisition cost.",
            "industry": "Services",
            "founded_year": 2018,
            "batch": "N/A",
            "status": "Private",
            "team_size": 9,
            "location": "Chicago, IL",
            "founders": ["Robert Kim"],
            "founder_experience": {
                "Robert Kim": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Corporate Gifts Inc", "position": "Sales", "years": "2015-2018"}
                    ],
                    "education": "DePaul University (BS Business)",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Niche Travel Blog Network",
            "description": "Aggregator of travel blogs for specific destinations. Low differentiation from existing platforms.",
            "industry": "Travel",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 3,
            "location": "Portland, OR",
            "founders": ["Jennifer Smith"],
            "founder_experience": {
                "Jennifer Smith": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "Portland State University (BS Communication)",
                    "technical": False,
                }
            },
            "source": "Wellfound",
            "label": 0
        },
        {
            "name": "Tutoring Marketplace",
            "description": "Platform connecting tutors with students for academic subjects. Overcrowded market with Chegg and Tutor.com.",
            "industry": "EdTech",
            "founded_year": 2018,
            "batch": "N/A",
            "status": "Private",
            "team_size": 11,
            "location": "Boston, MA",
            "founders": ["Amanda Lee"],
            "founder_experience": {
                "Amanda Lee": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Boston Public Schools", "position": "Teacher", "years": "2015-2018"}
                    ],
                    "education": "Boston University (BS Education)",
                    "technical": False,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "House Cleaning Booking",
            "description": "Booking system for house cleaning services. Highly local with limited scalability. Razor-thin margins.",
            "industry": "Services",
            "founded_year": 2020,
            "batch": "N/A",
            "status": "Private",
            "team_size": 7,
            "location": "Miami, FL",
            "founders": ["Isabella Garcia"],
            "founder_experience": {
                "Isabella Garcia": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Cleaning Company", "position": "Crew Lead", "years": "2018-2020"}
                    ],
                    "education": "Florida International University (BS Business)",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Small Business Accounting",
            "description": "Accounting software for freelancers. Competes with Quickbooks and FreshBooks. Difficult to differentiate.",
            "industry": "FinTech",
            "founded_year": 2017,
            "batch": "N/A",
            "status": "Private",
            "team_size": 12,
            "location": "San Diego, CA",
            "founders": ["Michael Chang"],
            "founder_experience": {
                "Michael Chang": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Small CPA Firm", "position": "Accountant", "years": "2013-2017"}
                    ],
                    "education": "San Diego State University (BS Accounting)",
                    "technical": False,
                }
            },
            "source": "Wellfound",
            "label": 0
        },
        {
            "name": "Local Delivery Service",
            "description": "Same-day delivery for local merchants. Competes with DoorDash and Uber Eats. High burn rate.",
            "industry": "Logistics",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 25,
            "location": "Phoenix, AZ",
            "founders": ["David Santos"],
            "founder_experience": {
                "David Santos": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Uber Eats", "position": "Operations Lead", "years": "2016-2019"}
                    ],
                    "education": "Arizona State University (BS Business)",
                    "technical": False,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "Pet Sitting Network",
            "description": "Connect pet owners with pet sitters. Niche market with intense local competition from Rover.",
            "industry": "Pet Services",
            "founded_year": 2018,
            "batch": "N/A",
            "status": "Private",
            "team_size": 6,
            "location": "Austin, TX",
            "founders": ["Sarah Thompson"],
            "founder_experience": {
                "Sarah Thompson": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "University of Texas (BS Animal Science)",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Yoga Class Booking",
            "description": "Simple booking system for yoga studios. Very niche with minimal differentiation.",
            "industry": "Wellness",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 5,
            "location": "Los Angeles, CA",
            "founders": ["Yoga Teacher Lisa"],
            "founder_experience": {
                "Yoga Teacher Lisa": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "Yoga Alliance Certification",
                    "technical": False,
                }
            },
            "source": "Wellfound",
            "label": 0
        },
        {
            "name": "Handmade Crafts Store",
            "description": "Online marketplace for handmade items. Competes with Etsy with no clear advantage.",
            "industry": "E-commerce",
            "founded_year": 2017,
            "batch": "N/A",
            "status": "Private",
            "team_size": 4,
            "location": "Brooklyn, NY",
            "founders": ["Maya Patel"],
            "founder_experience": {
                "Maya Patel": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "Parsons School of Design (BFA Crafts)",
                    "technical": False,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "Local Job Board",
            "description": "Job listing site for a single city. Insignificant scale compared to Indeed and LinkedIn.",
            "industry": "HR Tech",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 8,
            "location": "Dallas, TX",
            "founders": ["James Wilson"],
            "founder_experience": {
                "James Wilson": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Recruiting Firm", "position": "Recruiter", "years": "2015-2019"}
                    ],
                    "education": "Southern Methodist University (BS Business)",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Academic Paper Formatter",
            "description": "Tool to format academic papers. Limited market and redundant with existing tools.",
            "industry": "SaaS",
            "founded_year": 2020,
            "batch": "N/A",
            "status": "Private",
            "team_size": 3,
            "location": "Cambridge, MA",
            "founders": ["Dr. Robert Evans"],
            "founder_experience": {
                "Dr. Robert Evans": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Harvard", "position": "Postdoc", "years": "2018-2020"}
                    ],
                    "education": "Harvard University (PhD Physics)",
                    "technical": False,
                }
            },
            "source": "Wellfound",
            "label": 0
        },
        {
            "name": "Plant Identification App",
            "description": "Mobile app to identify plants using photos. Hobby project with limited commercial potential.",
            "industry": "Consumer App",
            "founded_year": 2020,
            "batch": "N/A",
            "status": "Private",
            "team_size": 2,
            "location": "Asheville, NC",
            "founders": ["Emma Green"],
            "founder_experience": {
                "Emma Green": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "University of North Carolina (BS Biology)",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Coupon Aggregator",
            "description": "Website collecting coupons from retailers. Passive income project with minimal value add.",
            "industry": "Consumer Services",
            "founded_year": 2018,
            "batch": "N/A",
            "status": "Private",
            "team_size": 2,
            "location": "Denver, CO",
            "founders": ["Coupon Hunter Bob"],
            "founder_experience": {
                "Coupon Hunter Bob": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "High School Diploma",
                    "technical": False,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "Blog About Tech",
            "description": "Technology blog covering news and reviews. Saturated market with no unique perspective.",
            "industry": "Media",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 3,
            "location": "San Francisco, CA",
            "founders": ["Tech Blogger John"],
            "founder_experience": {
                "Tech Blogger John": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "Self-taught",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Dropshipping Store",
            "description": "Dropshipping e-commerce store reselling generic products. Extremely low barriers to entry and differentiation.",
            "industry": "E-commerce",
            "founded_year": 2020,
            "batch": "N/A",
            "status": "Private",
            "team_size": 1,
            "location": "Unknown",
            "founders": ["Anonymous Seller"],
            "founder_experience": {
                "Anonymous Seller": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "High School Diploma",
                    "technical": False,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "Email Newsletter Service",
            "description": "Email template builder for newsletters. Redundant with MailChimp and Substack.",
            "industry": "SaaS",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 4,
            "location": "Austin, TX",
            "founders": ["David Brown"],
            "founder_experience": {
                "David Brown": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Web Agency", "position": "Developer", "years": "2015-2019"}
                    ],
                    "education": "Bootcamp (Web Development)",
                    "technical": True,
                }
            },
            "source": "Wellfound",
            "label": 0
        },
        {
            "name": "Resume Builder",
            "description": "Online tool to create resumes. Crowded market with Canva, Indeed, and dozens of others.",
            "industry": "SaaS",
            "founded_year": 2018,
            "batch": "N/A",
            "status": "Private",
            "team_size": 5,
            "location": "Seattle, WA",
            "founders": ["Career Coach Sara"],
            "founder_experience": {
                "Career Coach Sara": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Career Coaching", "position": "Coach", "years": "2012-2018"}
                    ],
                    "education": "University of Washington (BS Business)",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Niche Forum Community",
            "description": "Online forum for enthusiasts of a specific hobby. Limited network effects and declining forum traffic.",
            "industry": "Social Media",
            "founded_year": 2015,
            "batch": "N/A",
            "status": "Private",
            "team_size": 2,
            "location": "Portland, OR",
            "founders": ["Forum Moderator Steve"],
            "founder_experience": {
                "Forum Moderator Steve": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "High School Diploma",
                    "technical": False,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "Local Weather App",
            "description": "Weather application with local forecasts. Redundant with existing Weather.com and native OS apps.",
            "industry": "Consumer App",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 3,
            "location": "Boulder, CO",
            "founders": ["Weather Enthusiast Tom"],
            "founder_experience": {
                "Weather Enthusiast Tom": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "University of Colorado (BS Meteorology)",
                    "technical": False,
                }
            },
            "source": "Wellfound",
            "label": 0
        },
        {
            "name": "Apartment Rental Platform",
            "description": "Apartment listing aggregator for a single city. Competes with Zillow and Craigslist with no advantage.",
            "industry": "Real Estate",
            "founded_year": 2018,
            "batch": "N/A",
            "status": "Private",
            "team_size": 6,
            "location": "Austin, TX",
            "founders": ["Landlord Larry"],
            "founder_experience": {
                "Landlord Larry": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "University of Texas (BS Real Estate)",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Movie Review Aggregator",
            "description": "Website aggregating movie reviews. Redundant with IMDB and Rotten Tomatoes.",
            "industry": "Media",
            "founded_year": 2017,
            "batch": "N/A",
            "status": "Private",
            "team_size": 2,
            "location": "Los Angeles, CA",
            "founders": ["Film Buff Marcus"],
            "founder_experience": {
                "Film Buff Marcus": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "USC (BA Film Studies)",
                    "technical": False,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "Stock Tips Newsletter",
            "description": "Email newsletter with stock trading tips. Unaccredited advice with legal liability.",
            "industry": "Finance",
            "founded_year": 2020,
            "batch": "N/A",
            "status": "Private",
            "team_size": 1,
            "location": "Wall Street",
            "founders": ["Day Trader Joe"],
            "founder_experience": {
                "Day Trader Joe": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "High School Diploma",
                    "technical": False,
                }
            },
            "source": "Wellfound",
            "label": 0
        },
        {
            "name": "Noisy Neighborhood Forum",
            "description": "Neighborhood social network for local issues. Ultra-niche with minimal expansion potential.",
            "industry": "Social Media",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 3,
            "location": "Portland, OR",
            "founders": ["Neighborhood Hero"],
            "founder_experience": {
                "Neighborhood Hero": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "Community College",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Recipe Collection App",
            "description": "App to save and organize recipes. Heavily fragmented market with thousands of competitors.",
            "industry": "Consumer App",
            "founded_year": 2020,
            "batch": "N/A",
            "status": "Private",
            "team_size": 2,
            "location": "Austin, TX",
            "founders": ["Home Chef Alex"],
            "founder_experience": {
                "Home Chef Alex": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "Culinary Institute (Certificate)",
                    "technical": False,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "Expense Tracker",
            "description": "Personal expense tracking app. Saturated market with Mint, YNAB, and dozens of others.",
            "industry": "FinTech",
            "founded_year": 2018,
            "batch": "N/A",
            "status": "Private",
            "team_size": 4,
            "location": "Denver, CO",
            "founders": ["Budget Conscious Brian"],
            "founder_experience": {
                "Budget Conscious Brian": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "University of Colorado (BS Finance)",
                    "technical": False,
                }
            },
            "source": "Wellfound",
            "label": 0
        },
        {
            "name": "Reading List Manager",
            "description": "App to manage personal reading lists. Nice-to-have tool with weak monetization.",
            "industry": "Consumer App",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 1,
            "location": "Seattle, WA",
            "founders": ["Book Lover Lisa"],
            "founder_experience": {
                "Book Lover Lisa": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "University of Washington (BS English)",
                    "technical": False,
                }
            },
            "source": "IndieHackers",
            "label": 0
        },
        {
            "name": "Password Manager",
            "description": "Password management tool. Dominated by 1Password, Bitwarden, and LastPass.",
            "industry": "Security",
            "founded_year": 2017,
            "batch": "N/A",
            "status": "Private",
            "team_size": 3,
            "location": "San Francisco, CA",
            "founders": ["Security Expert Chris"],
            "founder_experience": {
                "Security Expert Chris": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [
                        {"name": "Security Firm", "position": "Consultant", "years": "2012-2017"}
                    ],
                    "education": "UC Berkeley (BS Computer Science)",
                    "technical": True,
                }
            },
            "source": "AngelList",
            "label": 0
        },
        {
            "name": "Side Hustle Job Board",
            "description": "Platform for side gigs and freelance work. Competes with Fiverr and Upwork but with no differentiation.",
            "industry": "Marketplace",
            "founded_year": 2019,
            "batch": "N/A",
            "status": "Private",
            "team_size": 5,
            "location": "Los Angeles, CA",
            "founders": ["Freelance King Marcus"],
            "founder_experience": {
                "Freelance King Marcus": {
                    "roles": ["Founder/CEO"],
                    "previous_companies": [],
                    "education": "High School Diploma",
                    "technical": False,
                }
            },
            "source": "Wellfound",
            "label": 0
        },
    ]
    
    def __init__(self):
        """Initialize synthetic data generator."""
        log.info("✓ SyntheticDataGenerator initialized with 100 companies (50 YC + 50 non-YC) + founder experience")
    
    def generate_dataset(self) -> pd.DataFrame:
        """
        Generate complete synthetic dataset with founder work experience.
        
        Returns:
            DataFrame with 100 companies (50 YC + 50 non-YC)
        """
        log.info("Generating synthetic dataset with comprehensive founder experience...")
        
        # Combine YC and non-YC data
        all_companies = self.YC_COMPANIES_SYNTHETIC + self.NON_YC_COMPANIES_SYNTHETIC
        
        all_data = []
        
        for company in all_companies:
            
            # Extract founder experience data
            founder_exp = company.get("founder_experience", {})
            
            # Build previous companies list
            previous_companies_list = []
            if founder_exp:
                for founder_name, exp_data in founder_exp.items():
                    for company_info in exp_data.get("previous_companies", []):
                        prev_company = f"{company_info['name']} ({company_info['position']})"
                        if prev_company not in previous_companies_list:
                            previous_companies_list.append(prev_company)
            
            # Build education list
            education_list = []
            if founder_exp:
                for founder_name, exp_data in founder_exp.items():
                    education = exp_data.get("education", "")
                    if education and education not in education_list:
                        education_list.append(education)
            
            # Check if any founder has technical background
            has_technical = False
            if founder_exp:
                has_technical = any([exp_data.get("technical", False) for exp_data in founder_exp.values()])
            
            # Create row
            row = {
                "name": company["name"],
                "description": company["description"],
                "industry": company["industry"],
                "founded_year": company.get("founded_year", 2020),
                "batch": company.get("batch", "N/A"),
                "status": company.get("status", "Private"),
                "team_size": company.get("team_size", 0),
                "location": company.get("location", "Unknown"),
                "source": company["source"],
                "label": company["label"],
                
                # Founder information
                "founder_count": len(company.get("founders", [])),
                "founder_names": " | ".join(company.get("founders", [])),
                "founder_previous_companies": " | ".join(previous_companies_list) if previous_companies_list else "None",
                "founder_education": " | ".join(education_list) if education_list else "Unknown",
                "founder_technical_background": has_technical,
            }
            
            all_data.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(all_data)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['name'])
        
        # Shuffle
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        log.info(f"✓ Generated dataset shape: {df.shape}")
        log.info(f"  Positive (YC): {(df['label'] == 1).sum()}")
        log.info(f"  Negative (Non-YC): {(df['label'] == 0).sum()}")
        log.info(f"\n✓ Dataset columns:")
        for col in df.columns:
            log.info(f"  - {col}")
        
        return df