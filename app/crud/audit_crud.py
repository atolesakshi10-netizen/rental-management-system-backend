from app.models import AuditLog


def create_audit_log(
    db,
    user_email,
    action
):

    print("AUDIT LOG FUNCTION CALLED")

    log = AuditLog(
        user_email=user_email,
        action=action
    )

    db.add(log)
    db.commit()

    print("AUDIT LOG SAVED")

    return log