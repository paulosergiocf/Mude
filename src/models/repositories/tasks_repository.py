from src.config.db_sessions import create_session
from src.models.tasks import Task

class TaskRepository:

    @staticmethod
    def get_task_by_id(id, status=None) -> Task:
        with create_session() as session:
            if status != None:
                data =  session.query(Task).where(Task.id == id, Task.status==status).first()
            else:
                data =  session.query(Task).where(Task.id == id).first()
            return data

    @staticmethod
    def get_all() -> list[Task]:
        with create_session() as session:
            data =  session.query(Task).all()

            return data
    
    @staticmethod
    def create_task(name: str, description: str, start_date: str, end_date: str) -> Task:
        task: Task = Task(
                name=name,
                description= description,
                start_date=start_date,
                end_date=end_date,
            )

        with create_session() as session:
            session.add(task)
            session.commit()
        
        return task

    @staticmethod
    def update_task(task: Task) -> Task:
        with create_session() as session:
            try:
                merged_task = session.merge(task)
                session.commit()
                session.refresh(merged_task)
                return merged_task
            except Exception as e:
                session.rollback()
                raise e
    

    @staticmethod
    def delete_task(task):
        with create_session() as session:
            if task:
                session.delete(task)
                session.commit()
