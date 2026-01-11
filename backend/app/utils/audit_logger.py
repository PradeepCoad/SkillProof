from models.audit_log import AuditLog

def log_action(
    db,
    action : str,
    entity: str,
    message: str = None,
    user_id: int = None,
    entity_id: int = None
):
    log = AuditLog(
        action=action,
        entity=entity,
        entity_id=entity_id,
        message=message,
        user_id=user_id
    )
    db.add(log)
    db.commit()