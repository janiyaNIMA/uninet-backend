from datetime import datetime
import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='student') # student, excom, admin
    full_name = db.Column(db.String(120), default='Jane Doe')
    phone = db.Column(db.String(50), default='+94 77 123 4567')
    university = db.Column(db.String(150), default='Wayamba University of Sri Lanka')
    faculty = db.Column(db.String(150), default='Faculty of Applied Sciences')
    degree_stream = db.Column(db.String(150), default='BSc (Hons) in Computer Science')
    batch = db.Column(db.String(50), default='Batch of 2022/23')
    badge_tier = db.Column(db.String(50), default='Gold')
    total_points = db.Column(db.Integer, default=530)
    next_tier_points = db.Column(db.Integer, default=600)
    skills = db.Column(db.Text, default='["Full-Stack Development","Cloud Computing","AI & Machine Learning","Leadership","Project Management"]')
    interests = db.Column(db.Text, default='["Hackathons","Open Source","WIE Leadership","UI/UX Design"]')
    academic_modules = db.Column(db.Text, default='["CS3102 - Web Engineering","CS3204 - Artificial Intelligence","CS3105 - Cloud Architecture"]')
    public_profile_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        def parse_json(val):
            try:
                return json.loads(val) if val else []
            except Exception:
                return [x.strip() for x in val.split(',')] if val else []

        return {
            "id": self.id,
            "username": self.username,
            "name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "university": self.university,
            "faculty": self.faculty,
            "degreeStream": self.degree_stream,
            "batch": self.batch,
            "badgeTier": self.badge_tier,
            "totalPoints": self.total_points,
            "nextTierPoints": self.next_tier_points,
            "skills": parse_json(self.skills),
            "interests": parse_json(self.interests),
            "academicModules": parse_json(self.academic_modules),
            "publicProfileEnabled": self.public_profile_enabled
        }

class Society(db.Model):
    __tablename__ = 'societies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    short_name = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    past_events = db.Column(db.Text, default='[]')
    skills = db.Column(db.Text, default='[]')
    excom = db.Column(db.Text, default='[]')
    member_count = db.Column(db.Integer, default=100)
    color = db.Column(db.String(30), default='#1565C0')
    is_wie = db.Column(db.Boolean, default=False)
    mentor_available = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        def parse_json(val):
            try:
                return json.loads(val) if val else []
            except Exception:
                return []

        return {
            "id": self.id,
            "name": self.name,
            "shortName": self.short_name or self.name,
            "category": self.category,
            "description": self.description,
            "pastEvents": parse_json(self.past_events),
            "skills": parse_json(self.skills),
            "excom": parse_json(self.excom),
            "memberCount": self.member_count,
            "color": self.color,
            "isWIE": self.is_wie,
            "hasApplied": False
        }

class SocietyApplication(db.Model):
    __tablename__ = 'society_applications'

    id = db.Column(db.Integer, primary_key=True)
    society_id = db.Column(db.Integer, db.ForeignKey('societies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    applicant_name = db.Column(db.String(120))
    applicant_email = db.Column(db.String(120))
    status = db.Column(db.String(30), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WIEMentor(db.Model):
    __tablename__ = 'wie_mentors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(150))
    initials = db.Column(db.String(10))
    tags = db.Column(db.Text, default='[]')
    contact_email = db.Column(db.String(120))

    def to_dict(self):
        try:
            parsed_tags = json.loads(self.tags) if self.tags else []
        except Exception:
            parsed_tags = [t.strip() for t in self.tags.split(',')] if self.tags else []
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "initials": self.initials,
            "tags": parsed_tags,
            "contactEmail": self.contact_email
        }

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    society_name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50))
    module = db.Column(db.String(100))
    date = db.Column(db.String(50))
    match_score = db.Column(db.Integer, default=80)
    image = db.Column(db.String(255))
    tags = db.Column(db.String(255)) # comma-separated tags
    description = db.Column(db.Text)
    society_id = db.Column(db.Integer, db.ForeignKey('societies.id'), nullable=True)
    location = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "society": self.society_name,
            "category": self.category,
            "module": self.module,
            "date": self.date,
            "matchScore": self.match_score,
            "image": self.image,
            "tags": [t.strip() for t in self.tags.split(',')] if self.tags else [],
            "description": self.description,
            "location": self.location,
            "isRegistered": False
        }

class EventRegistration(db.Model):
    __tablename__ = 'event_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    registration_code = db.Column(db.String(50), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

class Badge(db.Model):
    __tablename__ = 'badges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    tier = db.Column(db.String(30), default='Gold')
    unlocked = db.Column(db.Boolean, default=True)
    points = db.Column(db.Integer, default=100)
    earned_date = db.Column(db.String(50))
    icon = db.Column(db.String(20), default='🏆')
    description = db.Column(db.Text)
    issuer = db.Column(db.String(100), default='UniNet Campus')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "tier": self.tier,
            "unlocked": self.unlocked,
            "points": self.points,
            "earnedDate": self.earned_date,
            "icon": self.icon,
            "description": self.description
        }

class ResumeActivity(db.Model):
    __tablename__ = 'resume_activities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    role = db.Column(db.String(150), nullable=False)
    organization = db.Column(db.String(150), nullable=False)
    event = db.Column(db.String(150))
    category = db.Column(db.String(50))
    period = db.Column(db.String(50))
    verified = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "organization": self.organization,
            "event": self.event,
            "category": self.category,
            "period": self.period,
            "verified": self.verified
        }

class RecruitmentCandidate(db.Model):
    __tablename__ = 'recruitment_candidates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    initials = db.Column(db.String(10))
    badge_level = db.Column(db.String(30), default='Gold')
    points = db.Column(db.Integer, default=500)
    match_score = db.Column(db.Integer, default=90)
    applied_for = db.Column(db.String(150))
    type = db.Column(db.String(30), default='applicant') # applicant, ai_suggested
    academic_background = db.Column(db.String(150))
    skills = db.Column(db.Text, default='[]')
    past_contributions = db.Column(db.Text)
    rating = db.Column(db.Float, default=4.5)
    status = db.Column(db.String(30), default='Pending')

    def to_dict(self):
        try:
            parsed_skills = json.loads(self.skills) if self.skills else []
        except Exception:
            parsed_skills = [s.strip() for s in self.skills.split(',')] if self.skills else []
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "initials": self.initials,
            "badgeLevel": self.badge_level,
            "points": self.points,
            "matchScore": self.match_score,
            "appliedFor": self.applied_for,
            "type": self.type,
            "academicBackground": self.academic_background,
            "skills": parsed_skills,
            "pastContributions": self.past_contributions,
            "rating": self.rating,
            "status": self.status
        }

class RecruitmentDrive(db.Model):
    __tablename__ = 'recruitment_drives'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    role_type = db.Column(db.String(50))
    target_audience = db.Column(db.String(150))
    applicants_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(30), default='Active')
    deadline = db.Column(db.String(50))
    boost_reach = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "roleType": self.role_type,
            "targetAudience": self.target_audience,
            "applicants": self.applicants_count,
            "status": self.status,
            "deadline": self.deadline,
            "boostReach": self.boost_reach
        }

class UserSettings(db.Model):
    __tablename__ = 'user_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    email_notifications = db.Column(db.Boolean, default=True)
    in_app_alerts = db.Column(db.Boolean, default=True)
    recruitment_notifs = db.Column(db.Boolean, default=False)
    society_broadcasts = db.Column(db.Boolean, default=True)
    theme_mode = db.Column(db.String(20), default='light')
    contrast_option = db.Column(db.String(20), default='standard')
    privacy_public_profile = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "email_notifications": self.email_notifications,
            "inAppAlerts": self.in_app_alerts,
            "emailUpdates": self.email_notifications,
            "recruitmentNotifs": self.recruitment_notifs,
            "societyBroadcasts": self.society_broadcasts,
            "theme_mode": self.theme_mode,
            "contrast_option": self.contrast_option,
            "privacy_public_profile": self.privacy_public_profile
        }

