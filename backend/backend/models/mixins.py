from sqlalchemy import Column, DateTime, func


class TimestampMixin(object):
    created_at = Column(DateTime, nullable=False, server_default=func.now())
