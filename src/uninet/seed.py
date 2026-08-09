import json
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.uninet.main import create_app
from src.uninet.models import (
    db, User, Society, WIEMentor, Event, Badge, ResumeActivity,
    RecruitmentCandidate, RecruitmentDrive, UserSettings
)

app = create_app()

MOCK_EVENTS = [
  {
    "id": 1,
    "title": "IEEE Cloud Computing Workshop",
    "society_name": "IEEE CS Chapter",
    "category": "workshop",
    "module": "Computer Science",
    "date": "2026-08-20",
    "match_score": 95,
    "image": "https://picsum.photos/seed/cloud/400/200",
    "tags": "Cloud,AWS,DevOps",
    "description": "Hands-on cloud computing workshop covering AWS fundamentals and DevOps pipelines."
  },
  {
    "id": 2,
    "title": "HackElite 2026 – Hackathon",
    "society_name": "IEEE SBC WUSL",
    "category": "hackathon",
    "module": "Engineering",
    "date": "2026-09-05",
    "match_score": 88,
    "image": "https://picsum.photos/seed/hackathon/400/200",
    "tags": "AI,Innovation,Team",
    "description": "Annual 24-hour inter-university hackathon focusing on AI-driven products."
  },
  {
    "id": 3,
    "title": "WIE Leadership Summit",
    "society_name": "IEEE WIE AG",
    "category": "seminar",
    "module": "All Faculties",
    "date": "2026-08-28",
    "match_score": 82,
    "image": "https://picsum.photos/seed/wie/400/200",
    "tags": "Leadership,WIE,Mentorship",
    "description": "Inspiring talks from industry women leaders and alumnae mentors."
  },
  {
    "id": 4,
    "title": "Inter-Faculty Sports Meet",
    "society_name": "Sports Council",
    "category": "sports",
    "module": "All Faculties",
    "date": "2026-09-10",
    "match_score": 65,
    "image": "https://picsum.photos/seed/sports/400/200",
    "tags": "Sports,Health,Team",
    "description": "Annual sports meet featuring cricket, football, track & field events."
  },
  {
    "id": 5,
    "title": "Full-Stack Dev Bootcamp",
    "society_name": "FOSS Club",
    "category": "workshop",
    "module": "IT",
    "date": "2026-08-25",
    "match_score": 91,
    "image": "https://picsum.photos/seed/foss/400/200",
    "tags": "React,Node.js,Open Source",
    "description": "Comprehensive bootcamp on building React & Node.js web apps from scratch."
  },
  {
    "id": 6,
    "title": "Entrepreneurship Pitch Night",
    "society_name": "E-Club",
    "category": "seminar",
    "module": "Business",
    "date": "2026-09-01",
    "match_score": 74,
    "image": "https://picsum.photos/seed/eclub/400/200",
    "tags": "Startup,Pitch,Business",
    "description": "Pitch your student startup ideas to potential investors and mentors."
  }
]

MOCK_SOCIETIES = [
  {
    "id": 1,
    "name": "IEEE Student Branch Chapter",
    "short_name": "IEEE SBC",
    "category": "Technical",
    "description": "The flagship IEEE student branch driving engineering excellence through workshops, hackathons, guest lectures, and industry connections.",
    "past_events": json.dumps(["HackElite 2025", "PCB Design Workshop", "Industry Talk: AI in Robotics"]),
    "skills": json.dumps(["Leadership", "Project Management", "Technical Writing", "Networking"]),
    "excom": json.dumps([
        { "name": "Asel Perera", "role": "Chairperson", "initials": "AP" },
        { "name": "Kasun Silva", "role": "Vice Chair", "initials": "KS" },
        { "name": "Nimal Fernando", "role": "Secretary", "initials": "NF" },
        { "name": "Dilan Raj", "role": "Treasurer", "initials": "DR" }
    ]),
    "member_count": 120,
    "color": "#1565C0",
    "is_wie": False
  },
  {
    "id": 2,
    "name": "IEEE Women in Engineering",
    "short_name": "IEEE WIE",
    "category": "Inclusivity",
    "description": "Empowering women in technology through mentorship programmes, leadership workshops, career guidance, and a supportive community network.",
    "past_events": json.dumps(["WIE Leadership Summit", "Girls in STEM Outreach", "Alumnae Mentorship Day"]),
    "skills": json.dumps(["Mentorship", "Public Speaking", "Diversity Focus", "Leadership"]),
    "excom": json.dumps([
        { "name": "Sanduni Wickrama", "role": "Chair", "initials": "SW" },
        { "name": "Thilini Jayawardena", "role": "Vice Chair", "initials": "TJ" },
        { "name": "Ayesha Haris", "role": "Secretary", "initials": "AH" }
    ]),
    "member_count": 75,
    "color": "#7B1FA2",
    "is_wie": True
  },
  {
    "id": 3,
    "name": "IEEE Computer Society Chapter",
    "short_name": "IEEE CS",
    "category": "Technical",
    "description": "Focused on software development, cloud computing, and artificial intelligence through hands-on hackathons and open-source project sprints.",
    "past_events": json.dumps(["Cloud Computing Bootcamp", "Competitive Programming Fest", "Open Source Day"]),
    "skills": json.dumps(["Full-Stack Dev", "AI & ML", "Cloud Computing", "Problem Solving"]),
    "excom": json.dumps([
        { "name": "Ruwan Bandara", "role": "Chair", "initials": "RB" },
        { "name": "Ishara Mendis", "role": "Vice Chair", "initials": "IM" },
        { "name": "Chamari Dias", "role": "Secretary", "initials": "CD" }
    ]),
    "member_count": 95,
    "color": "#2E7D32",
    "is_wie": False
  },
  {
    "id": 4,
    "name": "FOSS Community",
    "short_name": "FOSS",
    "category": "Technical",
    "description": "Promoting open source software culture through Linux install events, code contribution sprints, and developer mentorship initiatives.",
    "past_events": json.dumps(["Linux Install Fest", "GSOC Prep Workshop", "Hacktoberfest Sprint"]),
    "skills": json.dumps(["Open Source", "Linux Admin", "Git & GitHub", "Community Build"]),
    "excom": json.dumps([
        { "name": "Lahiru Gunaratne", "role": "Lead", "initials": "LG" },
        { "name": "Piyumi Senanayake", "role": "Co-Lead", "initials": "PS" }
    ]),
    "member_count": 55,
    "color": "#E65100",
    "is_wie": False
  },
  {
    "id": 5,
    "name": "Entrepreneurship Club",
    "short_name": "E-Club",
    "category": "Business",
    "description": "Nurturing student startup founders through business pitch nights, incubator workshops, investor networking, and venture mentoring.",
    "past_events": json.dumps(["Pitch Night Vol.3", "Startup Weekend", "Business Model Canvas Workshop"]),
    "skills": json.dumps(["Entrepreneurship", "Business Strategy", "Pitching Skills", "Finance Basics"]),
    "excom": json.dumps([
        { "name": "Malith Jayasuriya", "role": "President", "initials": "MJ" },
        { "name": "Hiruni Wijesinghe", "role": "VP", "initials": "HW" },
        { "name": "Ravindu Perera", "role": "Secretary", "initials": "RP" }
    ]),
    "member_count": 65,
    "color": "#F57F17",
    "is_wie": False
  },
  {
    "id": 6,
    "name": "Sports Council",
    "short_name": "Sports",
    "category": "Sports",
    "description": "Organising campus tournaments, inter-university sports meets, and fitness sessions to promote student wellness and athletic achievement.",
    "past_events": json.dumps(["Inter-Faculty Cricket", "Badminton Championship", "Annual Sports Meet"]),
    "skills": json.dumps(["Teamwork", "Event Planning", "Fitness Training", "Time Management"]),
    "excom": json.dumps([
        { "name": "Chathura Madawala", "role": "Captain", "initials": "CM" },
        { "name": "Sachini Liyanage", "role": "Vice Captain", "initials": "SL" }
    ]),
    "member_count": 140,
    "color": "#00695C",
    "is_wie": False
  }
]

MOCK_WIE_MENTORS = [
  {
    "id": 1,
    "name": "Dr. Chamila Rathnayake",
    "role": "Faculty Mentor · Senior Lecturer",
    "initials": "CR",
    "tags": json.dumps(["AI", "Research"]),
    "contact_email": "chamila@wusl.ac.lk"
  },
  {
    "id": 2,
    "name": "Eng. Dilini Senanayake",
    "role": "Alumnae Mentor · Software Engineer @ WSO2",
    "initials": "DS",
    "tags": json.dumps(["Full-Stack", "Career"]),
    "contact_email": "dilini@wso2.com"
  },
  {
    "id": 3,
    "name": "Sanduni Wickrama",
    "role": "WIE Chair · Final Year Undergraduate",
    "initials": "SW",
    "tags": json.dumps(["Leadership", "WIE"]),
    "contact_email": "sanduni@wusl.ac.lk"
  }
]

MOCK_BADGES = [
  {
    "id": 1,
    "title": "Hackathon Hero",
    "category": "Innovation",
    "tier": "Gold",
    "unlocked": True,
    "points": 150,
    "earned_date": "2026-05-12",
    "icon": "🏆",
    "description": "Participated and placed in top 3 in HackElite 2025."
  },
  {
    "id": 2,
    "title": "Cloud Specialist",
    "category": "Technical",
    "tier": "Silver",
    "unlocked": True,
    "points": 100,
    "earned_date": "2026-06-20",
    "icon": "☁️",
    "description": "Completed IEEE CS Cloud Computing workshop series."
  },
  {
    "id": 3,
    "title": "WIE Trailblazer",
    "category": "Leadership",
    "tier": "Gold",
    "unlocked": True,
    "points": 200,
    "earned_date": "2026-07-04",
    "icon": "🌟",
    "description": "Led outreach initiative for female undergraduates in STEM."
  },
  {
    "id": 4,
    "title": "Open Source Contributor",
    "category": "Community",
    "tier": "Bronze",
    "unlocked": True,
    "points": 80,
    "earned_date": "2026-07-18",
    "icon": "💻",
    "description": "Submitted 3+ merged PRs during FOSS Hacktoberfest."
  },
  {
    "id": 5,
    "title": "Event Coordinator",
    "category": "Management",
    "tier": "Platinum",
    "unlocked": False,
    "points": 250,
    "earned_date": None,
    "icon": "📋",
    "description": "Organise 5 major campus events as ExCom or OC lead."
  },
  {
    "id": 6,
    "title": "Master Mentor",
    "category": "Mentorship",
    "tier": "Platinum",
    "unlocked": False,
    "points": 300,
    "earned_date": None,
    "icon": "🎓",
    "description": "Complete 20 hours of peer or junior student mentorship."
  }
]

MOCK_RESUME_ACTIVITIES = [
  {
    "id": 1,
    "role": "Lead Organiser & Student Lead",
    "organization": "IEEE Student Branch Chapter",
    "event": "HackElite 2025 Hackathon",
    "category": "Leadership & Management",
    "period": "Mar 2025 – May 2025",
    "verified": True
  },
  {
    "id": 2,
    "role": "Participant & Runner-Up",
    "organization": "IEEE Computer Society",
    "event": "Cloud Computing Sprint",
    "category": "Technical Skill",
    "period": "Jun 2026",
    "verified": True
  },
  {
    "id": 3,
    "role": "WIE Ambassador",
    "organization": "IEEE Women in Engineering",
    "event": "STEM Outreach Programme",
    "category": "Community & Mentorship",
    "period": "Jul 2026",
    "verified": True
  },
  {
    "id": 4,
    "role": "Sub-Committee Member",
    "organization": "Entrepreneurship Club",
    "event": "Pitch Night Vol. 3",
    "category": "Business & Soft Skills",
    "period": "Jan 2026",
    "verified": True
  }
]

MOCK_CANDIDATES = [
  {
    "id": 1,
    "name": "Kavindi Bandara",
    "email": "kavindi@wusl.ac.lk",
    "initials": "KB",
    "badge_level": "Gold",
    "points": 620,
    "match_score": 96,
    "applied_for": "HackElite 2026 OC Lead",
    "type": "applicant",
    "academic_background": "BSc Hons Computer Science (3rd Year)",
    "skills": json.dumps(["Full-Stack Dev", "Event Management", "UI/UX"]),
    "past_contributions": "Sub-committee Lead for PCB Workshop 2025; 4 hackathon wins.",
    "rating": 5.0,
    "status": "Pending"
  },
  {
    "id": 2,
    "name": "Sahan Perera",
    "email": "sahan@wusl.ac.lk",
    "initials": "SP",
    "badge_level": "Silver",
    "points": 410,
    "match_score": 92,
    "applied_for": "HackElite 2026 Logistics OC",
    "type": "applicant",
    "academic_background": "BSc Industrial Management (2nd Year)",
    "skills": json.dumps(["Logistics", "Budgeting", "Vendor Relations"]),
    "past_contributions": "Coordinator for Sports Meet 2025; Active E-Club member.",
    "rating": 4.5,
    "status": "Pending"
  },
  {
    "id": 3,
    "name": "Dilini Wickramasinghe",
    "email": "dilini@wusl.ac.lk",
    "initials": "DW",
    "badge_level": "Platinum",
    "points": 890,
    "match_score": 98,
    "applied_for": "IEEE CS Vice Chair",
    "type": "ai_suggested",
    "academic_background": "BSc Hons Software Engineering (3rd Year)",
    "skills": json.dumps(["Cloud Architecture", "AI/ML", "Team Leadership"]),
    "past_contributions": "FOSS Community Lead; GSOC Contributor; WIE Senior Ambassador.",
    "rating": 5.0,
    "status": "Pending"
  },
  {
    "id": 4,
    "name": "Tharindu Fernando",
    "email": "tharindu@wusl.ac.lk",
    "initials": "TF",
    "badge_level": "Bronze",
    "points": 220,
    "match_score": 78,
    "applied_for": "HackElite 2026 Design OC",
    "type": "applicant",
    "academic_background": "BSc Applied Sciences (1st Year)",
    "skills": json.dumps(["Graphic Design", "Figma", "Video Editing"]),
    "past_contributions": "Created promotional flyers for IEEE CS Bootcamp.",
    "rating": 4.0,
    "status": "Pending"
  },
  {
    "id": 5,
    "name": "Nipuni Jayawardena",
    "email": "nipuni@wusl.ac.lk",
    "initials": "NJ",
    "badge_level": "Gold",
    "points": 580,
    "match_score": 94,
    "applied_for": "WIE Mentorship OC Lead",
    "type": "ai_suggested",
    "academic_background": "BSc Hons Computer Science (3rd Year)",
    "skills": json.dumps(["Mentorship", "Public Speaking", "Diversity Outreach"]),
    "past_contributions": "WIE Leadership Summit Lead Coordinator; Alumnae Liaison.",
    "rating": 5.0,
    "status": "Pending"
  }
]

MOCK_DRIVES = [
  {
    "id": 1,
    "title": "HackElite 2026 Organizing Committee",
    "role_type": "OC Recruitment",
    "target_audience": "All Undergraduate Batches",
    "applicants_count": 34,
    "status": "Active",
    "deadline": "2026-08-30"
  },
  {
    "id": 2,
    "title": "IEEE CS Chapter Vice Chair & Secretary",
    "role_type": "ExCom Vacancy",
    "target_audience": "CS / IT Batches (2nd & 3rd Year)",
    "applicants_count": 12,
    "status": "Active",
    "deadline": "2026-09-10"
  },
  {
    "id": 3,
    "title": "WIE Mentorship Programme Coordinators",
    "role_type": "OC Recruitment",
    "target_audience": "Female Undergraduates",
    "applicants_count": 18,
    "status": "Closed",
    "deadline": "2026-08-01"
  }
]

def seed_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # 1. Seed main demo user
        demo_user = User(
            id=1,
            username="jane",
            email="jane@wusl.ac.lk",
            password_hash="pbkdf2:sha256:260000$devpassword$",
            role="student",
            full_name="Jane Doe",
            phone="+94 77 123 4567",
            university="Wayamba University of Sri Lanka",
            faculty="Faculty of Applied Sciences",
            degree_stream="BSc (Hons) in Computer Science",
            batch="Batch of 2022/23",
            badge_tier="Gold",
            total_points=530,
            next_tier_points=600,
            skills=json.dumps(["Full-Stack Development", "Cloud Computing", "AI & Machine Learning", "Leadership", "Project Management"]),
            interests=json.dumps(["Hackathons", "Open Source", "WIE Leadership", "UI/UX Design"]),
            academic_modules=json.dumps(["CS3102 - Web Engineering", "CS3204 - Artificial Intelligence", "CS3105 - Cloud Architecture"]),
            public_profile_enabled=True
        )
        db.session.add(demo_user)

        # 2. Seed UserSettings
        demo_settings = UserSettings(
            id=1,
            user_id=1,
            email_notifications=True,
            in_app_alerts=True,
            recruitment_notifs=False,
            society_broadcasts=True,
            theme_mode="light",
            contrast_option="standard",
            privacy_public_profile=True
        )
        db.session.add(demo_settings)

        # 3. Seed Societies
        for s in MOCK_SOCIETIES:
            soc = Society(
                id=s["id"],
                name=s["name"],
                short_name=s["short_name"],
                category=s["category"],
                description=s["description"],
                past_events=s["past_events"],
                skills=s["skills"],
                excom=s["excom"],
                member_count=s["member_count"],
                color=s["color"],
                is_wie=s["is_wie"]
            )
            db.session.add(soc)

        # 4. Seed WIE Mentors
        for m in MOCK_WIE_MENTORS:
            mentor = WIEMentor(
                id=m["id"],
                name=m["name"],
                role=m["role"],
                initials=m["initials"],
                tags=m["tags"],
                contact_email=m["contact_email"]
            )
            db.session.add(mentor)

        # 5. Seed Events
        for item in MOCK_EVENTS:
            event = Event(
                id=item["id"],
                title=item["title"],
                society_name=item["society_name"],
                category=item["category"],
                module=item["module"],
                date=item["date"],
                match_score=item["match_score"],
                image=item["image"],
                tags=item["tags"],
                description=item["description"],
                society_id=1
            )
            db.session.add(event)

        # 6. Seed Badges
        for b in MOCK_BADGES:
            badge = Badge(
                id=b["id"],
                user_id=1,
                title=b["title"],
                category=b["category"],
                tier=b["tier"],
                unlocked=b["unlocked"],
                points=b["points"],
                earned_date=b["earned_date"],
                icon=b["icon"],
                description=b["description"]
            )
            db.session.add(badge)

        # 7. Seed Resume Activities
        for a in MOCK_RESUME_ACTIVITIES:
            act = ResumeActivity(
                id=a["id"],
                user_id=1,
                role=a["role"],
                organization=a["organization"],
                event=a["event"],
                category=a["category"],
                period=a["period"],
                verified=a["verified"]
            )
            db.session.add(act)

        # 8. Seed Recruitment Candidates
        for c in MOCK_CANDIDATES:
            cand = RecruitmentCandidate(
                id=c["id"],
                name=c["name"],
                email=c["email"],
                initials=c["initials"],
                badge_level=c["badge_level"],
                points=c["points"],
                match_score=c["match_score"],
                applied_for=c["applied_for"],
                type=c["type"],
                academic_background=c["academic_background"],
                skills=c["skills"],
                past_contributions=c["past_contributions"],
                rating=c["rating"],
                status=c["status"]
            )
            db.session.add(cand)

        # 9. Seed Recruitment Drives
        for d in MOCK_DRIVES:
            drive = RecruitmentDrive(
                id=d["id"],
                title=d["title"],
                role_type=d["role_type"],
                target_audience=d["target_audience"],
                applicants_count=d["applicants_count"],
                status=d["status"],
                deadline=d["deadline"]
            )
            db.session.add(drive)
            
        db.session.commit()
        print("UniNet SQLite Database successfully seeded with all mock records.")

if __name__ == '__main__':
    seed_database()

