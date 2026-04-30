"""Seed script — populates NIST CSF 2.0, ISO 27001:2022, and CIS Controls v8 into the database."""
from app.database import SessionLocal
from app.models.framework import Framework, Domain, Control

FRAMEWORKS = [
    {
        "name": "NIST Cybersecurity Framework",
        "version": "2.0",
        "slug": "nist-csf-2",
        "description": "NIST CSF 2.0 provides a flexible framework to manage and reduce cybersecurity risk.",
        "domains": [
            {
                "name": "Govern", "code": "GV",
                "controls": [
                    {"control_id": "GV.OC-01", "title": "Organisational context", "severity": "high"},
                    {"control_id": "GV.RM-01", "title": "Risk management strategy", "severity": "critical"},
                    {"control_id": "GV.PO-01", "title": "Policy establishment", "severity": "high"},
                ]
            },
            {
                "name": "Identify", "code": "ID",
                "controls": [
                    {"control_id": "ID.AM-01", "title": "Asset inventory — hardware", "severity": "high"},
                    {"control_id": "ID.AM-02", "title": "Asset inventory — software", "severity": "high"},
                    {"control_id": "ID.RA-01", "title": "Risk identification", "severity": "critical"},
                    {"control_id": "ID.RA-02", "title": "Threat and vulnerability information", "severity": "high"},
                ]
            },
            {
                "name": "Protect", "code": "PR",
                "controls": [
                    {"control_id": "PR.AA-01", "title": "Access control — identities managed", "severity": "critical"},
                    {"control_id": "PR.AA-02", "title": "Remote access managed", "severity": "high"},
                    {"control_id": "PR.DS-01", "title": "Data-at-rest protection", "severity": "critical"},
                    {"control_id": "PR.DS-02", "title": "Data-in-transit protection", "severity": "critical"},
                    {"control_id": "PR.PS-01", "title": "Configuration management", "severity": "high"},
                    {"control_id": "PR.IR-01", "title": "Secure network environments", "severity": "high"},
                ]
            },
            {
                "name": "Detect", "code": "DE",
                "controls": [
                    {"control_id": "DE.CM-01", "title": "Networks monitored", "severity": "high"},
                    {"control_id": "DE.CM-03", "title": "Personnel activity monitored", "severity": "medium"},
                    {"control_id": "DE.AE-02", "title": "Anomalous events analysed", "severity": "high"},
                ]
            },
            {
                "name": "Respond", "code": "RS",
                "controls": [
                    {"control_id": "RS.MA-01", "title": "Incident response plan", "severity": "critical"},
                    {"control_id": "RS.CO-02", "title": "Internal stakeholder reporting", "severity": "medium"},
                    {"control_id": "RS.AN-03", "title": "Incident analysis", "severity": "high"},
                ]
            },
            {
                "name": "Recover", "code": "RC",
                "controls": [
                    {"control_id": "RC.RP-01", "title": "Recovery plan execution", "severity": "critical"},
                    {"control_id": "RC.CO-03", "title": "Recovery communications", "severity": "medium"},
                ]
            },
        ]
    },
    {
        "name": "ISO/IEC 27001",
        "version": "2022",
        "slug": "iso-27001-2022",
        "description": "ISO 27001:2022 specifies requirements for establishing, implementing, and maintaining an ISMS.",
        "domains": [
            {
                "name": "Organisational Controls", "code": "A.5",
                "controls": [
                    {"control_id": "A.5.1", "title": "Policies for information security", "severity": "high"},
                    {"control_id": "A.5.9", "title": "Inventory of information assets", "severity": "high"},
                    {"control_id": "A.5.15", "title": "Access control policy", "severity": "critical"},
                    {"control_id": "A.5.23", "title": "Information security for cloud services", "severity": "high"},
                    {"control_id": "A.5.24", "title": "Information security incident management", "severity": "critical"},
                ]
            },
            {
                "name": "People Controls", "code": "A.6",
                "controls": [
                    {"control_id": "A.6.1", "title": "Screening", "severity": "medium"},
                    {"control_id": "A.6.3", "title": "Information security awareness", "severity": "high"},
                    {"control_id": "A.6.8", "title": "Information security event reporting", "severity": "medium"},
                ]
            },
            {
                "name": "Physical Controls", "code": "A.7",
                "controls": [
                    {"control_id": "A.7.1", "title": "Physical security perimeters", "severity": "high"},
                    {"control_id": "A.7.8", "title": "Equipment siting and protection", "severity": "medium"},
                ]
            },
            {
                "name": "Technological Controls", "code": "A.8",
                "controls": [
                    {"control_id": "A.8.2", "title": "Privileged access rights", "severity": "critical"},
                    {"control_id": "A.8.5", "title": "Secure authentication", "severity": "critical"},
                    {"control_id": "A.8.7", "title": "Protection against malware", "severity": "high"},
                    {"control_id": "A.8.9", "title": "Configuration management", "severity": "high"},
                    {"control_id": "A.8.12", "title": "Data leakage prevention", "severity": "high"},
                    {"control_id": "A.8.24", "title": "Use of cryptography", "severity": "high"},
                ]
            },
        ]
    },
    {
        "name": "CIS Controls",
        "version": "v8",
        "slug": "cis-controls-v8",
        "description": "CIS Controls v8 is a prioritised set of actions to protect against cyber attacks.",
        "domains": [
            {
                "name": "Basic Controls (IG1)", "code": "CIS-IG1",
                "controls": [
                    {"control_id": "CIS-1.1", "title": "Establish and maintain detailed enterprise asset inventory", "severity": "high"},
                    {"control_id": "CIS-2.1", "title": "Establish and maintain software inventory", "severity": "high"},
                    {"control_id": "CIS-3.3", "title": "Configure data access control lists", "severity": "critical"},
                    {"control_id": "CIS-4.1", "title": "Establish and maintain secure configuration process", "severity": "high"},
                    {"control_id": "CIS-5.2", "title": "Use unique passwords", "severity": "critical"},
                ]
            },
            {
                "name": "Foundational Controls (IG2)", "code": "CIS-IG2",
                "controls": [
                    {"control_id": "CIS-6.2", "title": "Establish access granting process", "severity": "high"},
                    {"control_id": "CIS-6.3", "title": "Establish access revoking process", "severity": "high"},
                    {"control_id": "CIS-10.2", "title": "Perform automated backups", "severity": "high"},
                    {"control_id": "CIS-12.1", "title": "Ensure network infrastructure up-to-date", "severity": "high"},
                    {"control_id": "CIS-13.1", "title": "Centralise security event alerting", "severity": "high"},
                ]
            },
            {
                "name": "Organisational Controls (IG3)", "code": "CIS-IG3",
                "controls": [
                    {"control_id": "CIS-17.1", "title": "Designate personnel to manage incident handling", "severity": "critical"},
                    {"control_id": "CIS-17.4", "title": "Establish and maintain incident response process", "severity": "critical"},
                    {"control_id": "CIS-18.1", "title": "Establish and maintain penetration testing programme", "severity": "medium"},
                ]
            },
        ]
    },
]


def seed():
    db = SessionLocal()
    try:
        if db.query(Framework).count() > 0:
            print("Frameworks already seeded, skipping.")
            return
        for fw_data in FRAMEWORKS:
            domains_data = fw_data.pop("domains")
            fw = Framework(**fw_data)
            db.add(fw)
            db.flush()
            for d_data in domains_data:
                controls_data = d_data.pop("controls")
                domain = Domain(**d_data, framework_id=fw.id)
                db.add(domain)
                db.flush()
                for c_data in controls_data:
                    control = Control(**c_data, domain_id=domain.id)
                    db.add(control)
        db.commit()
        print(f"Seeded {len(FRAMEWORKS)} frameworks successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
