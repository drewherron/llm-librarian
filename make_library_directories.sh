#!/bin/bash
# ==============================================================================
# THE DREWEY DECIMAL LIBRARY STRUCTURE
#
# This directory structure is based on the types of books I have or at least am
# likely to have in the future. Most category numbers (aside from 000)
# accurately follow the Dewey Decimal System, but are only used on the first
# two directories in the paths, for more flexibility. When you can't figure out
# where to put a new book or category, looking up the official DDC number
# should almost always work well enough. This is just a starting point, and
# directories can be added and deleted as needed.
# ==============================================================================

# Set the root directory for the ebook library.
ROOT_DIR="./Library"

# An array of all directories to be created.
DIRS=(
  # ------------------------------------------------------------------------------
  # 000: INFORMATION TECHNOLOGY & COMPUTER SCIENCE
  # ------------------------------------------------------------------------------

  # 001: Theoretical foundations and academic CS
  "$ROOT_DIR/000_Information_Technology/001_Foundations/Computer_Science_Theory"
  "$ROOT_DIR/000_Information_Technology/001_Foundations/Algorithms_Data_Structures"
  "$ROOT_DIR/000_Information_Technology/001_Foundations/Computer_Architecture"
  "$ROOT_DIR/000_Information_Technology/001_Foundations/Mathematics_for_Computing"
  "$ROOT_DIR/000_Information_Technology/001_Foundations/Compilers_Language_Theory"
  "$ROOT_DIR/000_Information_Technology/001_Foundations/Computer_Graphics"
  "$ROOT_DIR/000_Information_Technology/001_Foundations/Human_Computer_Interaction"

  # 002: The infrastructure layer - what everything runs on
  "$ROOT_DIR/000_Information_Technology/002_Systems_Infrastructure/Operating_Systems/Unix_Linux"
  "$ROOT_DIR/000_Information_Technology/002_Systems_Infrastructure/Operating_Systems/BSD"
  "$ROOT_DIR/000_Information_Technology/002_Systems_Infrastructure/Operating_Systems/Windows"
  "$ROOT_DIR/000_Information_Technology/002_Systems_Infrastructure/Operating_Systems/Theory_Design"
  "$ROOT_DIR/000_Information_Technology/002_Systems_Infrastructure/Databases/PostgreSQL"
  "$ROOT_DIR/000_Information_Technology/002_Systems_Infrastructure/Databases/NoSQL"
  "$ROOT_DIR/000_Information_Technology/002_Systems_Infrastructure/Computer_Networks"
  "$ROOT_DIR/000_Information_Technology/002_Systems_Infrastructure/Distributed_Systems"
  "$ROOT_DIR/000_Information_Technology/002_Systems_Infrastructure/Hardware_Embedded"
  "$ROOT_DIR/000_Information_Technology/002_Systems_Infrastructure/Storage_File_Systems"

  # 003: The craft of writing code
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Programming_Fundamentals"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Software_Engineering/Design_Patterns"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Software_Engineering/Testing_QA"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Software_Engineering/Debugging_Performance"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Software_Engineering/Agile_Methodologies"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Software_Engineering/Clean_Code"

  # Languages: Organized alphabetically for easy browsing
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/Assembly"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/C"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/C++"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/Rust"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/Go"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/Java"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/Kotlin"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/Swift"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/Python"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/JavaScript"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/TypeScript"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/Lisp"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/PHP"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/Haskell"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/Scala"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/Clojure"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/SQL"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/R"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/MATLAB"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/HTML_CSS"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/XML_JSON"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Languages/Markdown_LaTeX"
  "$ROOT_DIR/000_Information_Technology/003_Software_Development/Version_Control/Git"

  # 004: Building specific types of applications
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Web_Development/Frontend/React"
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Web_Development/Frontend/Vue"
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Web_Development/Frontend/Angular"
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Web_Development/Frontend/Next"  # Next.js, Nuxt, etc.
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Web_Development/Backend/Django"
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Web_Development/Backend/Flask"
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Web_Development/Backend/FastAPI"
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Web_Development/APIs/REST"
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Web_Development/APIs/GraphQL"
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Web_Development/APIs/gRPC"
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Mobile_Development/iOS"
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Mobile_Development/Android"
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Game_Development"
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Desktop_Applications"
  "$ROOT_DIR/000_Information_Technology/004_Application_Domains/Embedded_IoT"

  # 005: Everything data and AI
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/Data_Science/Statistics_Analysis"
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/Data_Science/Visualization"
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/Data_Engineering"
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/Big_Data/Spark"
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/Big_Data/Hadoop"
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/Big_Data/Streaming_Processing"  # Kafka, Flink, etc.
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/Machine_Learning/Classical_ML"
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/Machine_Learning/Deep_Learning"
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/Machine_Learning/Reinforcement_Learning"
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/Machine_Learning/MLOps"
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/AI_Applications/Natural_Language_Processing"
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/AI_Applications/Computer_Vision"
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/AI_Applications/Robotics"
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/AI_Applications/Generative_AI"
  "$ROOT_DIR/000_Information_Technology/005_Data_AI/AI_Ethics_Society"

  # 006: Security deserves its own top-level category
  "$ROOT_DIR/000_Information_Technology/006_Security/Cryptography"
  "$ROOT_DIR/000_Information_Technology/006_Security/Network_Security"
  "$ROOT_DIR/000_Information_Technology/006_Security/Web_Security"  # OWASP, XSS, CSRF, etc.
  "$ROOT_DIR/000_Information_Technology/006_Security/Mobile_Security"
  "$ROOT_DIR/000_Information_Technology/006_Security/Secure_Coding"
  "$ROOT_DIR/000_Information_Technology/006_Security/Penetration_Testing"
  "$ROOT_DIR/000_Information_Technology/006_Security/Exploit_Development"
  "$ROOT_DIR/000_Information_Technology/006_Security/Digital_Forensics"
  "$ROOT_DIR/000_Information_Technology/006_Security/Incident_Response"
  "$ROOT_DIR/000_Information_Technology/006_Security/Security_Operations"  # SOC, SIEM, threat hunting
  "$ROOT_DIR/000_Information_Technology/006_Security/OSINT_Reconnaissance"
  "$ROOT_DIR/000_Information_Technology/006_Security/Compliance_Governance"  # GDPR, HIPAA, SOC2, etc.
  "$ROOT_DIR/000_Information_Technology/006_Security/Privacy_Anonymity"

  # 007: Modern deployment and operations
  "$ROOT_DIR/000_Information_Technology/007_DevOps_Cloud/AWS"
  "$ROOT_DIR/000_Information_Technology/007_DevOps_Cloud/Azure"
  "$ROOT_DIR/000_Information_Technology/007_DevOps_Cloud/GCP"
  "$ROOT_DIR/000_Information_Technology/007_DevOps_Cloud/Docker"
  "$ROOT_DIR/000_Information_Technology/007_DevOps_Cloud/Kubernetes"
  "$ROOT_DIR/000_Information_Technology/007_DevOps_Cloud/Terraform"
  "$ROOT_DIR/000_Information_Technology/007_DevOps_Cloud/Ansible"
  "$ROOT_DIR/000_Information_Technology/007_DevOps_Cloud/CI_CD"  # Jenkins, GitHub Actions, GitLab CI
  "$ROOT_DIR/000_Information_Technology/007_DevOps_Cloud/Monitoring_Observability"
  "$ROOT_DIR/000_Information_Technology/007_DevOps_Cloud/Site_Reliability_Engineering"

  # 008: Computing paradigms that don't fit the standard stack
  "$ROOT_DIR/000_Information_Technology/008_Specialized_Computing/Blockchain_Cryptocurrency"
  "$ROOT_DIR/000_Information_Technology/008_Specialized_Computing/Quantum_Computing"
  "$ROOT_DIR/000_Information_Technology/008_Specialized_Computing/High_Performance_Computing"
  "$ROOT_DIR/000_Information_Technology/008_Specialized_Computing/Augmented_Virtual_Reality"
  "$ROOT_DIR/000_Information_Technology/008_Specialized_Computing/Edge_Fog_Computing"
  "$ROOT_DIR/000_Information_Technology/008_Specialized_Computing/Bioinformatics"

  # 009: The human side of technology
  "$ROOT_DIR/000_Information_Technology/009_Professional_Technology/Career_Development"
  "$ROOT_DIR/000_Information_Technology/009_Professional_Technology/Tech_Leadership_Management"
  "$ROOT_DIR/000_Information_Technology/009_Professional_Technology/Technical_Writing_Documentation"
  "$ROOT_DIR/000_Information_Technology/009_Professional_Technology/Interview_Preparation"
  "$ROOT_DIR/000_Information_Technology/009_Professional_Technology/Technology_Business"
  "$ROOT_DIR/000_Information_Technology/009_Professional_Technology/Ethics_Society"
  "$ROOT_DIR/000_Information_Technology/009_Professional_Technology/History_of_Computing"
  "$ROOT_DIR/000_Information_Technology/009_Professional_Technology/Open_Source_Communities"
  "$ROOT_DIR/000_Information_Technology/009_Professional_Technology/Knowledge_Management"  # PKM, Zettelkasten, GTD?

  # ------------------------------------------------------------------------------
  # 100: PHILOSOPHY & PSYCHOLOGY
  # ------------------------------------------------------------------------------
  "$ROOT_DIR/100_Philosophy_Psychology/110_Metaphysics"
  "$ROOT_DIR/100_Philosophy_Psychology/120_Epistemology"
  "$ROOT_DIR/100_Philosophy_Psychology/130_Parapsychology_Occultism"
  "$ROOT_DIR/100_Philosophy_Psychology/140_Philosophical_Schools"
  "$ROOT_DIR/100_Philosophy_Psychology/150_Psychology"
  "$ROOT_DIR/100_Philosophy_Psychology/160_Logic"
  "$ROOT_DIR/100_Philosophy_Psychology/170_Ethics"
  "$ROOT_DIR/100_Philosophy_Psychology/180_Ancient_Philosophy"
  "$ROOT_DIR/100_Philosophy_Psychology/190_Modern_Philosophy"

  # ------------------------------------------------------------------------------
  # 200: RELIGION
  # ------------------------------------------------------------------------------
  "$ROOT_DIR/200_Religion/210_Philosophy_of_Religion"
  "$ROOT_DIR/200_Religion/230_Christianity/Bible"
  "$ROOT_DIR/200_Religion/230_Christianity/Theology"
  "$ROOT_DIR/200_Religion/230_Christianity/History"
  "$ROOT_DIR/200_Religion/230_Christianity/Roman_Catholicism"
  "$ROOT_DIR/200_Religion/230_Christianity/Eastern_Orthodox"
  "$ROOT_DIR/200_Religion/230_Christianity/Lutheranism"
  "$ROOT_DIR/200_Religion/230_Christianity/Reformed"
  "$ROOT_DIR/200_Religion/292_Greek_Roman_Religion"
  "$ROOT_DIR/200_Religion/293_Germanic_Religion"
  "$ROOT_DIR/200_Religion/294_Buddhism"
  "$ROOT_DIR/200_Religion/294_Zen"
  "$ROOT_DIR/200_Religion/295_Hinduism"
  "$ROOT_DIR/200_Religion/296_Judaism"
  "$ROOT_DIR/200_Religion/297_Islam"
  "$ROOT_DIR/200_Religion/299_Atheism"
  "$ROOT_DIR/200_Religion/299_Shintoism"
  "$ROOT_DIR/200_Religion/299_Taoism"
  "$ROOT_DIR/200_Religion/299_Confucianism"
  "$ROOT_DIR/200_Religion/299_Native_American_Religions"
  "$ROOT_DIR/200_Religion/299_African_Religions"
  "$ROOT_DIR/200_Religion/299_Religious_Syncretism"
  "$ROOT_DIR/200_Religion/299_Afro_Brazilian_Religions"
  "$ROOT_DIR/200_Religion/299_Norse_Mythology"
  "$ROOT_DIR/200_Religion/299_Paganism_Wicca"

  # ------------------------------------------------------------------------------
  # 300: SOCIAL SCIENCES
  # ------------------------------------------------------------------------------

  "$ROOT_DIR/300_Social_Sciences/301_Anthropology"         # Cross-cultural studies, ethnography, human evolution, archaeology
  "$ROOT_DIR/300_Social_Sciences/302_Sociology"            # Social theory, social movements, class/inequality, modern institutions
  "$ROOT_DIR/300_Social_Sciences/306_Culture_Institutions" # Marriage customs, family structures, cultural practices
  "$ROOT_DIR/300_Social_Sciences/307_Communities"          # Urban planning, rural sociology, neighborhood studies
  "$ROOT_DIR/300_Social_Sciences/308_Groups_of_People"     # Ethnic studies, racial dynamics, nationality/citizenship
  "$ROOT_DIR/300_Social_Sciences/310_Statistics"           # Census data, population studies, social surveys

  # Politics: Theory, systems, and ideologies
  "$ROOT_DIR/300_Social_Sciences/320_Politics_Government/Political_Theory_Philosophy"
  "$ROOT_DIR/300_Social_Sciences/320_Politics_Government/Government_Systems"          # Democracy, Monarchy, Republics, Constitutions
  "$ROOT_DIR/300_Social_Sciences/320_Politics_Government/The_Political_Process"       # Elections, Activism, Political Parties
  "$ROOT_DIR/300_Social_Sciences/320_Politics_Government/International_Relations"     # Diplomacy, Foreign Policy, Geopolitics
  "$ROOT_DIR/300_Social_Sciences/320_Politics_Government/Political_Parties"           # Party systems and organization
  "$ROOT_DIR/300_Social_Sciences/320_Politics_Government/Political_Situations"        # Contemporary political issues
  "$ROOT_DIR/300_Social_Sciences/320_Politics_Government/Ideologies_and_Movements/Anarchism"
  "$ROOT_DIR/300_Social_Sciences/320_Politics_Government/Ideologies_and_Movements/Conservatism"
  "$ROOT_DIR/300_Social_Sciences/320_Politics_Government/Ideologies_and_Movements/Fascism"
  "$ROOT_DIR/300_Social_Sciences/320_Politics_Government/Ideologies_and_Movements/Liberalism"
  "$ROOT_DIR/300_Social_Sciences/320_Politics_Government/Ideologies_and_Movements/Libertarianism"
  "$ROOT_DIR/300_Social_Sciences/320_Politics_Government/Ideologies_and_Movements/Socialism_Communism"

  # Economics: Theory and practice
  "$ROOT_DIR/300_Social_Sciences/330_Economics/Economic_Philosophy"
  "$ROOT_DIR/300_Social_Sciences/330_Economics/Austrian_Economics"
  "$ROOT_DIR/300_Social_Sciences/330_Economics/Macroeconomics"
  "$ROOT_DIR/300_Social_Sciences/330_Economics/Microeconomics"
  "$ROOT_DIR/300_Social_Sciences/330_Economics/Personal_Finance"
  "$ROOT_DIR/300_Social_Sciences/330_Economics/International_Economics"

  # Law: Various legal domains
  "$ROOT_DIR/300_Social_Sciences/340_Law/International_Law"
  "$ROOT_DIR/300_Social_Sciences/340_Law/Constitutional_Law"
  "$ROOT_DIR/300_Social_Sciences/340_Law/Business_Law"
  "$ROOT_DIR/300_Social_Sciences/340_Law/Criminal_Law"

  "$ROOT_DIR/300_Social_Sciences/350_Public_Administration"

  # Military science and warfare
  "$ROOT_DIR/300_Social_Sciences/355_Military_Science/Army_Manuals"
  "$ROOT_DIR/300_Social_Sciences/355_Military_Science/Weapons_Training"
  "$ROOT_DIR/300_Social_Sciences/355_Military_Science/Intelligence_Operations"
  "$ROOT_DIR/300_Social_Sciences/355_Military_Science/Field_Tactics"

  # Social problems and services
  "$ROOT_DIR/300_Social_Sciences/360_Social_Problems_and_Services/Criminology"
  "$ROOT_DIR/300_Social_Sciences/360_Social_Problems_and_Services/Secret_Societies"
  "$ROOT_DIR/300_Social_Sciences/360_Social_Problems_and_Services/General_Clubs"
  "$ROOT_DIR/300_Social_Sciences/360_Social_Problems_and_Services/Insurance"
  "$ROOT_DIR/300_Social_Sciences/360_Social_Problems_and_Services/Associations"

  "$ROOT_DIR/300_Social_Sciences/370_Education"
  "$ROOT_DIR/300_Social_Sciences/380_Commerce_Communication"  # Trade, transportation, postal services

  # Customs, traditions, and folklore
  "$ROOT_DIR/300_Social_Sciences/390_Customs_Traditions/Scottish_Tartans"
  "$ROOT_DIR/300_Social_Sciences/390_Customs_Traditions/Fashion"
  "$ROOT_DIR/300_Social_Sciences/390_Customs_Traditions/Folklore"

  # ------------------------------------------------------------------------------
  # 400: LANGUAGE
  # ------------------------------------------------------------------------------

  # General linguistics applicable to all languages
  "$ROOT_DIR/400_Language/410_Linguistics/Writing_Systems"
  "$ROOT_DIR/400_Language/410_Linguistics/Etymology"
  "$ROOT_DIR/400_Language/410_Linguistics/Dictionaries"
  "$ROOT_DIR/400_Language/410_Linguistics/Phonology"
  "$ROOT_DIR/400_Language/410_Linguistics/Grammar"
  "$ROOT_DIR/400_Language/410_Linguistics/Semantics"
  "$ROOT_DIR/400_Language/410_Linguistics/Dialectology"
  "$ROOT_DIR/400_Language/410_Linguistics/Standard_Usage"
  "$ROOT_DIR/400_Language/410_Linguistics/Sign_Languages"
  "$ROOT_DIR/400_Language/410_Linguistics/Syntax"
  "$ROOT_DIR/400_Language/410_Linguistics/Morphology"
  "$ROOT_DIR/400_Language/410_Linguistics/Sociolinguistics"

  # English: The most detailed section for English-language materials
  "$ROOT_DIR/400_Language/420_English_Language/Writing_System"
  "$ROOT_DIR/400_Language/420_English_Language/Etymology"
  "$ROOT_DIR/400_Language/420_English_Language/Dictionaries"
  "$ROOT_DIR/400_Language/420_English_Language/Grammar"
  "$ROOT_DIR/400_Language/420_English_Language/Dialects"
  "$ROOT_DIR/400_Language/420_English_Language/Usage"

  # Germanic languages
  "$ROOT_DIR/400_Language/430_German_Language/Writing_System"
  "$ROOT_DIR/400_Language/430_German_Language/Etymology"
  "$ROOT_DIR/400_Language/430_German_Language/Dictionaries"
  "$ROOT_DIR/400_Language/430_German_Language/Grammar"
  "$ROOT_DIR/400_Language/430_German_Language/Dialects"
  "$ROOT_DIR/400_Language/430_German_Language/Usage"
  "$ROOT_DIR/400_Language/431_Dutch_Language"
  "$ROOT_DIR/400_Language/432_Norwegian_Language"
  "$ROOT_DIR/400_Language/433_Swedish_Language"
  "$ROOT_DIR/400_Language/434_Danish_Language"

  # Romance languages
  "$ROOT_DIR/400_Language/440_French_Language"
  "$ROOT_DIR/400_Language/450_Italian_Language"
  "$ROOT_DIR/400_Language/459_Romanian_Language"
  "$ROOT_DIR/400_Language/460_Spanish_Language"
  "$ROOT_DIR/400_Language/460_Galego_Language"
  "$ROOT_DIR/400_Language/469_Portuguese_Language/Portuguese"
  "$ROOT_DIR/400_Language/469_Portuguese_Language/Brazilian_Portuguese"

  # Classical languages
  "$ROOT_DIR/400_Language/470_Latin_Language"
  "$ROOT_DIR/400_Language/480_Greek_Language"

  # Slavic languages
  "$ROOT_DIR/400_Language/491_Russian_Language"

  # Semitic languages
  "$ROOT_DIR/400_Language/492_Arabic_Language/Writing_System"
  "$ROOT_DIR/400_Language/492_Arabic_Language/Dictionaries"
  "$ROOT_DIR/400_Language/492_Arabic_Language/Grammar"
  "$ROOT_DIR/400_Language/492_Arabic_Language/Dialects/Iraqi_Arabic"
  "$ROOT_DIR/400_Language/492_Arabic_Language/Dialects/Gulf_Arabic"
  "$ROOT_DIR/400_Language/492_Arabic_Language/Dialects/Levantine_Arabic"
  "$ROOT_DIR/400_Language/492_Arabic_Language/Dialects/Egyptian_Arabic"
  "$ROOT_DIR/400_Language/492_Arabic_Language/Dialects/Yemeni_Arabic"
  "$ROOT_DIR/400_Language/493_Hebrew_Language"

  # Turkic languages
  "$ROOT_DIR/400_Language/494_Turkish_Language"

  # East Asian languages
  "$ROOT_DIR/400_Language/495_Chinese_Language"
  "$ROOT_DIR/400_Language/495_Japanese_Language"
  "$ROOT_DIR/400_Language/495_Manchu_Language"
  "$ROOT_DIR/400_Language/495_Korean_Language"

  # African languages
  "$ROOT_DIR/400_Language/496_Swahili_Language"

  # Indo-Iranian languages
  "$ROOT_DIR/400_Language/497_Hindi_Language"
  "$ROOT_DIR/400_Language/497_Sanskrit_Language"
  "$ROOT_DIR/400_Language/497_Tibetan_Language"
  "$ROOT_DIR/400_Language/497_Persian_Language"

  # Southeast Asian languages
  "$ROOT_DIR/400_Language/498_Thai_Language"
  "$ROOT_DIR/400_Language/498_Vietnamese_Language"
  "$ROOT_DIR/400_Language/498_Indonesian_Language"

  # Other languages
  "$ROOT_DIR/400_Language/499_Hungarian_Language"
  "$ROOT_DIR/400_Language/499_Finnish_Language"
  "$ROOT_DIR/400_Language/499_Hawaiian_Language"
  "$ROOT_DIR/400_Language/499_Constructed_Languages/Esperanto"
  "$ROOT_DIR/400_Language/499_Constructed_Languages/Toki_Pona"
  "$ROOT_DIR/400_Language/499_Constructed_Languages/Tolkien"
  "$ROOT_DIR/400_Language/499_Other_Languages"

  # ------------------------------------------------------------------------------
  # 500: SCIENCE
  # Pure sciences - applied sciences go in 600s
  # ------------------------------------------------------------------------------
  "$ROOT_DIR/500_Science/510_Mathematics/Algebra"
  "$ROOT_DIR/500_Science/510_Mathematics/Analysis"
  "$ROOT_DIR/500_Science/510_Mathematics/Arithmetic"
  "$ROOT_DIR/500_Science/510_Mathematics/Calculus"
  "$ROOT_DIR/500_Science/510_Mathematics/Geometry"
  "$ROOT_DIR/500_Science/510_Mathematics/Linear_Algebra"
  "$ROOT_DIR/500_Science/510_Mathematics/Number_Theory"
  "$ROOT_DIR/500_Science/510_Mathematics/Probabilities_Statistics"
  "$ROOT_DIR/500_Science/510_Mathematics/Topology"
  "$ROOT_DIR/500_Science/510_Mathematics/Trigonometry"
  "$ROOT_DIR/500_Science/520_Astronomy"
  "$ROOT_DIR/500_Science/530_Physics"
  "$ROOT_DIR/500_Science/540_Chemistry"
  "$ROOT_DIR/500_Science/550_Earth_Sciences"
  "$ROOT_DIR/500_Science/560_Paleontology"
  "$ROOT_DIR/500_Science/570_Biology"
  "$ROOT_DIR/500_Science/580_Botany"
  "$ROOT_DIR/500_Science/590_Zoology"

  # ------------------------------------------------------------------------------
  # 600: TECHNOLOGY (Applied Sciences)
  # Practical applications of scientific knowledge
  # ------------------------------------------------------------------------------

  # Medicine and health
  "$ROOT_DIR/600_Technology/610_Medicine_Health/Diseases"
  "$ROOT_DIR/600_Technology/610_Medicine_Health/Human_Anatomy"          # Structure of the human body
  "$ROOT_DIR/600_Technology/610_Medicine_Health/Human_Physiology"       # Functions of the human body
  "$ROOT_DIR/600_Technology/610_Medicine_Health/Personal_Health/Dietetics"
  "$ROOT_DIR/600_Technology/610_Medicine_Health/Personal_Health/Meditation"
  "$ROOT_DIR/600_Technology/610_Medicine_Health/Personal_Health/Physical_Fitness"
  "$ROOT_DIR/600_Technology/610_Medicine_Health/Personal_Health/Yoga"
  "$ROOT_DIR/600_Technology/610_Medicine_Health/Pharmacology"

  # Engineering - Note: Electronics here is hardware, not computer science
  "$ROOT_DIR/600_Technology/620_Engineering/Civil_Engineering"
  "$ROOT_DIR/600_Technology/620_Engineering/Electronics/Arduino"
  "$ROOT_DIR/600_Technology/620_Engineering/Electronics/Home_Electronics"
  "$ROOT_DIR/600_Technology/620_Engineering/Electronics/Raspberry_Pi"
  "$ROOT_DIR/600_Technology/620_Engineering/Military_Engineering"
  "$ROOT_DIR/600_Technology/620_Engineering/Radio/Licensing"
  "$ROOT_DIR/600_Technology/620_Engineering/Radio/Morse_Code"
  "$ROOT_DIR/600_Technology/620_Engineering/Sound_Recording"
  "$ROOT_DIR/600_Technology/620_Engineering/Telephony"

  # Agriculture and farming
  "$ROOT_DIR/600_Technology/630_Agriculture/Animal_Husbandry"
  "$ROOT_DIR/600_Technology/630_Agriculture/Beekeeping"
  "$ROOT_DIR/600_Technology/630_Agriculture/Gardening"
  "$ROOT_DIR/600_Technology/630_Agriculture/Hunting_Fishing"

  # Management and business
  "$ROOT_DIR/600_Technology/650_Management/Accounting"
  "$ROOT_DIR/600_Technology/650_Management/Public_Relations"
  "$ROOT_DIR/600_Technology/650_Management/Shorthand"

  # Manufacturing and crafts
  "$ROOT_DIR/600_Technology/680_Manufacturing/Blacksmithing"
  "$ROOT_DIR/600_Technology/680_Manufacturing/Bookbinding"
  "$ROOT_DIR/600_Technology/680_Manufacturing/Candlemaking"
  "$ROOT_DIR/600_Technology/680_Manufacturing/Leather"
  "$ROOT_DIR/600_Technology/680_Manufacturing/Lockpicking"
  "$ROOT_DIR/600_Technology/680_Manufacturing/Woodworking"

  "$ROOT_DIR/600_Technology/690_Building_Construction/Earthship"

  # ------------------------------------------------------------------------------
  # 640: HOME AND FAMILY MANAGEMENT
  # ------------------------------------------------------------------------------
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Beverages/Beer"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Beverages/Coffee"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Beverages/Liquor"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Beverages/Tea"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Beverages/Wine"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/American_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Arabic_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Brazilian_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/British_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Chinese_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Ethiopian_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/French_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/German_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Indian_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Irish_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Italian_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Japanese_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Mexican_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Portuguese_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Romanian_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Russian_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Scandinavian_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Scottish_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Spanish_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Food_and_Drink/Cooking_Recipes/Thai_Cooking"
  "$ROOT_DIR/640_Home_and_Family/641_Tobacco"
  "$ROOT_DIR/640_Home_and_Family/642_Meals_Table_Service"           # Entertaining, formal dining, etiquette
  "$ROOT_DIR/640_Home_and_Family/643_Household_Equipment/Manuals"   # Home maintenance, appliances
  "$ROOT_DIR/640_Home_and_Family/644_Household_Utilities"           # Heating, lighting, plumbing
  "$ROOT_DIR/640_Home_and_Family/645_Household_Furnishings"         # Interior design, decoration, furniture
  "$ROOT_DIR/640_Home_and_Family/646_Sewing_Clothing/Knitting"
  "$ROOT_DIR/640_Home_and_Family/646_Style_Grooming"
  "$ROOT_DIR/640_Home_and_Family/648_Housekeeping"                  # Cleaning, organizing, home management
  "$ROOT_DIR/640_Home_and_Family/649_Child_Rearing"

  # ------------------------------------------------------------------------------
  # 700: THE ARTS
  # ------------------------------------------------------------------------------
  "$ROOT_DIR/700_Art/710_Landscape_Architecture"
  "$ROOT_DIR/700_Art/720_Architecture"
  "$ROOT_DIR/700_Art/730_Sculpture"
  "$ROOT_DIR/700_Art/740_Graphic_Arts/Calligraphy"
  "$ROOT_DIR/700_Art/750_Painting"
  "$ROOT_DIR/700_Art/770_Photography"
  "$ROOT_DIR/700_Art/777_Cinematography"

  # ------------------------------------------------------------------------------
  # 780: MUSIC
  # ------------------------------------------------------------------------------
  "$ROOT_DIR/780_Music/781_Music_Theory"
  "$ROOT_DIR/780_Music/780_Music_History"
  "$ROOT_DIR/780_Music/782_Vocal_Music"
  "$ROOT_DIR/780_Music/784_Instruments_Instrumental_Ensembles"      # Orchestral music
  "$ROOT_DIR/780_Music/785_Ensembles_Chamber_Music"                 # Small ensemble music

  # Keyboard instruments instruction
  "$ROOT_DIR/780_Music/786_Keyboard_Instruments/Organ"
  "$ROOT_DIR/780_Music/786_Keyboard_Instruments/Piano/Blues_Piano"
  "$ROOT_DIR/780_Music/786_Keyboard_Instruments/Piano/Classical_Piano"
  "$ROOT_DIR/780_Music/786_Keyboard_Instruments/Piano/Gospel_Piano"
  "$ROOT_DIR/780_Music/786_Keyboard_Instruments/Piano/Jazz_Piano"
  "$ROOT_DIR/780_Music/786_Keyboard_Instruments/Piano/Popular_Piano"
  "$ROOT_DIR/780_Music/786_Keyboard_Instruments/Piano/Ragtime_Piano"

  "$ROOT_DIR/780_Music/786_Percussion"

  # Stringed instruments instruction
  "$ROOT_DIR/780_Music/787_Stringed_Instruments/Bass"
  "$ROOT_DIR/780_Music/787_Stringed_Instruments/Bouzouki"
  "$ROOT_DIR/780_Music/787_Stringed_Instruments/Guitar/Blues_Guitar"
  "$ROOT_DIR/780_Music/787_Stringed_Instruments/Guitar/Bossa_Nova_Guitar"
  "$ROOT_DIR/780_Music/787_Stringed_Instruments/Guitar/Brazilian_Guitar"
  "$ROOT_DIR/780_Music/787_Stringed_Instruments/Guitar/Classical_Guitar"
  "$ROOT_DIR/780_Music/787_Stringed_Instruments/Guitar/Flamenco_Guitar"
  "$ROOT_DIR/780_Music/787_Stringed_Instruments/Guitar/Folk_Guitar"
  "$ROOT_DIR/780_Music/787_Stringed_Instruments/Guitar/Guitar_Construction"
  "$ROOT_DIR/780_Music/787_Stringed_Instruments/Guitar/Guitar_Repair_Maintenance"
  "$ROOT_DIR/780_Music/787_Stringed_Instruments/Guitar/Jazz_Guitar"
  "$ROOT_DIR/780_Music/787_Stringed_Instruments/Guitar/Rock_Guitar"
  "$ROOT_DIR/780_Music/787_Stringed_Instruments/Mandolin"

  # Wind instruments instruction
  "$ROOT_DIR/780_Music/788_Wind_Instruments/Bagpipes"
  "$ROOT_DIR/780_Music/788_Wind_Instruments/Flute"
  "$ROOT_DIR/780_Music/788_Wind_Instruments/Saxophone"
  "$ROOT_DIR/780_Music/788_Wind_Instruments/Tin_Whistle"
  "$ROOT_DIR/780_Music/788_Wind_Instruments/Trumpet"

  # Genre-based instruction (not instrument-specific)
  "$ROOT_DIR/780_Music/789_Traditions_Genres/Blues_Instruction"
  "$ROOT_DIR/780_Music/789_Traditions_Genres/Brazilian_Music_Instruction"
  "$ROOT_DIR/780_Music/789_Traditions_Genres/Celtic_Music_Instruction"
  "$ROOT_DIR/780_Music/789_Traditions_Genres/Jazz_Instruction"
  "$ROOT_DIR/780_Music/789_Traditions_Genres/World_Music_Instruction"

  # Sheet music collections by artist/composer
  "$ROOT_DIR/780_Music/789_Sheet_Music/Bach"
  "$ROOT_DIR/780_Music/789_Sheet_Music/Chopin"
  "$ROOT_DIR/780_Music/789_Sheet_Music/Antonio_Carlos_Jobim"
  "$ROOT_DIR/780_Music/789_Sheet_Music/John_Coltrane"
  "$ROOT_DIR/780_Music/789_Sheet_Music/Miles_Davis"

  # ------------------------------------------------------------------------------
  # 790: RECREATION & SPORTS
  # ------------------------------------------------------------------------------
  "$ROOT_DIR/790_Recreation/794_Chess"
  "$ROOT_DIR/790_Recreation/794_Go"
  "$ROOT_DIR/790_Recreation/796_Baseball"
  "$ROOT_DIR/790_Recreation/796_Combat_Sports/Aikido"
  "$ROOT_DIR/790_Recreation/796_Cycling"
  "$ROOT_DIR/790_Recreation/796_Football"
  "$ROOT_DIR/790_Recreation/796_Hiking_Camping"
  "$ROOT_DIR/790_Recreation/796_Hockey"
  "$ROOT_DIR/790_Recreation/796_Soccer"
  "$ROOT_DIR/790_Recreation/796_Wilderness_Survival"
  "$ROOT_DIR/790_Recreation/799_Archery"

  # ------------------------------------------------------------------------------
  # 800: LITERATURE
  # Organized by original language of composition, not geography
  # ------------------------------------------------------------------------------
  "$ROOT_DIR/800_Literature/810_English_Literature"
  "$ROOT_DIR/800_Literature/830_German_Literature"
  "$ROOT_DIR/800_Literature/840_French_Literature"
  "$ROOT_DIR/800_Literature/850_Italian_Literature"
  "$ROOT_DIR/800_Literature/860_Spanish_Literature"
  "$ROOT_DIR/800_Literature/869_Portuguese_Literature"
  "$ROOT_DIR/800_Literature/870_Latin_Literature"
  "$ROOT_DIR/800_Literature/880_Classical_Greek_Lit"
  "$ROOT_DIR/800_Literature/890_Other_Literatures"
  "$ROOT_DIR/800_Literature/891_Russian_Literature"
  "$ROOT_DIR/800_Literature/892_Arabic_Literature"
  "$ROOT_DIR/800_Literature/895_Chinese_Literature"
  "$ROOT_DIR/800_Literature/895_Japanese_Literature/Manga"
  "$ROOT_DIR/800_Literature/897_African_Literature"
  "$ROOT_DIR/800_Literature/899_Canadian_Literature"

  # ------------------------------------------------------------------------------
  # 900: HISTORY & GEOGRAPHY
  # ------------------------------------------------------------------------------
  "$ROOT_DIR/900_History/908_History_of_Groups"  # History of specific ethnic, social, or religious groups
  "$ROOT_DIR/900_History/909_World_History"
  "$ROOT_DIR/900_History/930_Ancient_History"
  "$ROOT_DIR/900_History/940_Europe/England"
  "$ROOT_DIR/900_History/940_Europe/Finland"
  "$ROOT_DIR/900_History/940_Europe/France"
  "$ROOT_DIR/900_History/940_Europe/Germany"
  "$ROOT_DIR/900_History/940_Europe/Ireland"
  "$ROOT_DIR/900_History/940_Europe/Italy"
  "$ROOT_DIR/900_History/940_Europe/Portugal"
  "$ROOT_DIR/900_History/940_Europe/Romania"
  "$ROOT_DIR/900_History/940_Europe/Scandinavia"
  "$ROOT_DIR/900_History/940_Europe/Scotland"
  "$ROOT_DIR/900_History/940_Europe/Spain"
  "$ROOT_DIR/900_History/950_Asia/China"
  "$ROOT_DIR/900_History/950_Asia/Iran"
  "$ROOT_DIR/900_History/950_Asia/Japan"
  "$ROOT_DIR/900_History/950_Asia/Middle_East/Iraq"
  "$ROOT_DIR/900_History/950_Asia/Middle_East/Israel"
  "$ROOT_DIR/900_History/950_Asia/Middle_East/Yemen"
  "$ROOT_DIR/900_History/950_Asia/South_Asia_India"
  "$ROOT_DIR/900_History/950_Asia/Southeast_Asia"
  "$ROOT_DIR/900_History/960_Africa"
  "$ROOT_DIR/900_History/970_North_America/Canada"
  "$ROOT_DIR/900_History/970_North_America/Cascadia"
  "$ROOT_DIR/900_History/970_North_America/Cuba"
  "$ROOT_DIR/900_History/970_North_America/Mexico"
  "$ROOT_DIR/900_History/970_North_America/United_States"
  "$ROOT_DIR/900_History/980_South_America/Argentina"
  "$ROOT_DIR/900_History/980_South_America/Brazil"
  "$ROOT_DIR/900_History/990_Oceania/Australia"
  "$ROOT_DIR/900_History/990_Oceania/New_Zealand"

  # ------------------------------------------------------------------------------
  # 910: GEOGRAPHY & TRAVEL
  # ------------------------------------------------------------------------------
  "$ROOT_DIR/910_Geography_Travel/910_Geography"
  "$ROOT_DIR/910_Geography_Travel/911_Historical_Geography"

  # Travel guides by region
  "$ROOT_DIR/910_Geography_Travel/914_Travel_Europe/Scotland"
  "$ROOT_DIR/910_Geography_Travel/914_Travel_Europe/England"
  "$ROOT_DIR/910_Geography_Travel/914_Travel_Europe/France"
  "$ROOT_DIR/910_Geography_Travel/914_Travel_Europe/Italy"
  "$ROOT_DIR/910_Geography_Travel/914_Travel_Europe/Spain_Portugal"
  "$ROOT_DIR/910_Geography_Travel/914_Travel_Europe/Germany"
  "$ROOT_DIR/910_Geography_Travel/914_Travel_Europe/Scandinavia"
  "$ROOT_DIR/910_Geography_Travel/914_Travel_Europe/Other_Europe"
  "$ROOT_DIR/910_Geography_Travel/915_Travel_Asia/China"
  "$ROOT_DIR/910_Geography_Travel/915_Travel_Asia/Japan"
  "$ROOT_DIR/910_Geography_Travel/915_Travel_Asia/India"
  "$ROOT_DIR/910_Geography_Travel/915_Travel_Asia/Middle_East"
  "$ROOT_DIR/910_Geography_Travel/915_Travel_Asia/Southeast_Asia"
  "$ROOT_DIR/910_Geography_Travel/916_Travel_Africa"
  "$ROOT_DIR/910_Geography_Travel/917_Travel_North_America/Canada"
  "$ROOT_DIR/910_Geography_Travel/917_Travel_North_America/United_States"
  "$ROOT_DIR/910_Geography_Travel/917_Travel_North_America/Mexico"
  "$ROOT_DIR/910_Geography_Travel/917_Travel_North_America/Central_America"
  "$ROOT_DIR/910_Geography_Travel/917_Travel_North_America/Caribbean"
  "$ROOT_DIR/910_Geography_Travel/918_Travel_South_America/Brazil"
  "$ROOT_DIR/910_Geography_Travel/918_Travel_South_America/Argentina"
  "$ROOT_DIR/910_Geography_Travel/919_Travel_Oceania/Australia"
  "$ROOT_DIR/910_Geography_Travel/919_Travel_Oceania/New_Zealand"

  # ------------------------------------------------------------------------------
  # OTHER
  # ------------------------------------------------------------------------------
  "$ROOT_DIR/Childrens_Books"
  "$ROOT_DIR/Unclassified"
)

# Create each directory
for dir in "${DIRS[@]}"; do
  mkdir -p "$dir"
done

echo "✅ Ebook library structure created at: $ROOT_DIR"
echo ""
echo "000 Information Technology: Computer science, programming, AI, security, cloud/DevOps"
echo "100 Philosophy & Psychology: Metaphysics, ethics, logic, philosophical schools, psychology"
echo "200 Religion: World religions, theology, mythology, atheism, spiritual traditions"
echo "300 Social Sciences: Politics, economics, law, sociology, anthropology, education"
echo "400 Language: Linguistics, specific languages by family, grammar, dictionaries"
echo "500 Science: Pure sciences - mathematics, physics, chemistry, biology, astronomy"
echo "600 Technology: Applied sciences - medicine, engineering, agriculture, manufacturing"
echo "640 Home & Family: Cooking, housekeeping, child-rearing, sewing, interior design"
echo "700 Arts: Architecture, painting, sculpture, photography, graphic arts"
echo "780 Music: Theory, instruments, genres, sheet music, instruction books"
echo "790 Recreation: Sports, games, outdoor activities, martial arts"
echo "800 Literature: Fiction and poetry by original language of composition"
echo "900 History: Historical periods and events by geographical region"
echo "910 Geography & Travel: Maps, travel guides, geographical studies"
echo ""
echo "- Languages: 400s organized by family, not geography"
echo "- Pure sciences: 500s (theoretical) vs Applied sciences: 600s (practical)"
echo "- Literature: 800s by original language, not author nationality"
echo "- No biography section - place in most relevant subject/category"
