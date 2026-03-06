def route_query(query):
    query = query.lower()

    # IT
    if any(word in query for word in ["wifi", "internet", "portal", "ums", "email", "network"]):
        return "IT"

    # Admissions
    elif any(word in query for word in ["admission", "apply", "eligibility", "documents"]):
        return "Admissions"

    # Examination
    elif any(word in query for word in ["exam", "result", "reappear", "revaluation", "scrutiny"]):
        return "Examination"

    # Fees and Account
    elif any(word in query for word in ["fee", "payment", "refund", "scholarship", "reimbursement"]):
        return "Fees_and_Account"

    # Academics
    elif any(word in query for word in ["attendance", "timetable", "syllabus", "academic", "class"]):
        return "Academics"

    # Residential Services
    elif any(word in query for word in ["hostel", "mess", "laundry", "room", "maintenance"]):
        return "Residential_Services"

    # Security and Safety
    elif any(word in query for word in ["theft", "harassment", "fight", "security", "threat"]):
        return "Security_and_Safety"

    # Library
    elif any(word in query for word in ["library", "book", "journal", "plagiarism"]):
        return "Library"

    # Placements
    elif any(word in query for word in ["placement", "internship", "company", "offer"]):
        return "Placements"

    # International Affair
    elif any(word in query for word in ["visa", "frro", "international", "exchange"]):
        return "International_Affair"

    # Research & Development
    elif any(word in query for word in ["phd", "research", "thesis", "publication", "grant"]):
        return "Division_of_Research_and_Development"

    else:
        return "General_Inquiry"