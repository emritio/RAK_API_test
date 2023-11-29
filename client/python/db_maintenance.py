from database import db

def create_metric_id_column():
    # Add the metric_id column to the system_metrics table
    db.engine.execute(
        'drop table SystemMetrics;drop table Users;'
    )
