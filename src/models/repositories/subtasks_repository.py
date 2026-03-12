from src.config.db_sessions import create_session
from src.models.subtasks import SubTask
from src.models.tasks import Task
from src.util.date_util import DateUtil
from datetime import datetime, timedelta
import sqlalchemy as sa
class SubTaskRepository:

    @staticmethod
    def get_subtask_by_task(task_id) -> list[SubTask]:
        with create_session() as session:
            data =  session.query(SubTask).where(SubTask.group_task_id == id)
            return data
  
    @staticmethod
    def get_all() -> list[SubTask]:
        with create_session() as session:
            data =  session.query(SubTask).all()
            return data

    @staticmethod
    def get_subtask_by_task_and_date(tasks, date) -> list[SubTask]:
        with create_session() as session:
            data =  session.query(SubTask).filter(SubTask.due_date == today).all() if task_ids else None
            return data

    @staticmethod
    def get_subtask_by_tasks_and_filter_date(tasks, week_start, week_end):
        task_ids = [task.id for task in tasks]
        with create_session() as session:
            subtasks = (
            session.query(SubTask)
            .filter(
                SubTask.group_task_id.in_(task_ids),
                SubTask.due_date >= week_start,
                SubTask.due_date <= week_end
            ).order_by('due_date')
            .all()
        ) if task_ids else session.query(SubTask).filter(sa.false())

        return subtasks

    @staticmethod
    def get_subtask_by_task_and_filter_date(task, week_start, week_end):
        with create_session() as session:
            subtasks = (
            session.query(SubTask)
            .filter(
                SubTask.group_task_id == task.id,
                SubTask.due_date >= week_start,
                SubTask.due_date <= week_end
            )
        ) if task else session.query(SubTask).filter(sa.false())

        return subtasks

    @staticmethod
    def get_percentage_task(task):
        with create_session() as session:
            completed = list()
            subtasks: list[SubTask] = session.query(SubTask).where(SubTask.group_task_id == task.id)
            if subtasks.count() == 0:
                return 0
            for subtask in subtasks:
                if subtask.status:
                    completed.append(subtask)

            percentage = int((len(completed) / subtasks.count()) * 100)
            return percentage

    @staticmethod
    def completed_subtasks_for_week_percentage(subtasks):
        if subtasks.count() == 0:
            return 0

        completed = list()
        for subtask in subtasks:
            if subtask.status:
                completed.append(subtask)
   
        return int((len(completed) / subtasks.count()) * 100)


    @staticmethod
    def list_weeks(task: Task):
        weeks =  DateUtil.week_list(task.start_date, task.end_date)
        weeks_percentage = []
        for week in weeks:
            subtasks  = SubTaskRepository.get_subtask_by_task_and_filter_date(task, week[0], week[1])
            percentage = SubTaskRepository.completed_subtasks_for_week_percentage(subtasks)
            weeks_percentage.append((week, percentage))
        return weeks_percentage

    @staticmethod
    def list_week(tasks, week=0, next_week=True):
        today = datetime.today().date()
        first_day = today + timedelta(weeks=week) if next_week else today - timedelta(weeks=week)
        weeks =  DateUtil.get_week_range(first_day)
        
        weeks_percentage = []
        for week in weeks:
            subtask_for_week  = SubTaskRepository.get_subtask_by_tasks_and_filter_date(tasks, weeks[0], weeks[1])
            list_group_by_date = {}
            if subtask_for_week:
                for subtask in subtask_for_week:
                    due_date_str = subtask.due_date.strftime('%A | %Y-%m-%d')
                    if due_date_str not in list_group_by_date:
                        list_group_by_date[due_date_str] = []
                    list_group_by_date[due_date_str].append(subtask)
                subtask_for_week = list_group_by_date

        
        return list_group_by_date

    @staticmethod
    def create_subtask(description: str, due_date: str, task: Task):
        date = datetime.strptime(due_date, '%Y-%m-%d').date()
        while True:
            subtask: SubTask = SubTask(description= description, due_date=date, group_task_id=task.id)      
            if DateUtil.is_date_greater(date=date, end_date=task.end_date):
                break

            with create_session() as session:
                session.add(subtask)
                session.commit()
                session.refresh(subtask)
            
            date = DateUtil.get_next_week_date(date)

    @staticmethod
    def update_all_subtask(subtask: SubTask, description: str) -> SubTask:
        date = datetime.strptime(str(subtask.due_date), '%Y-%m-%d').date()
        subtasks = []
        with create_session() as session:
            while True:
                subtask_filter = None
                if DateUtil.is_date_greater(date=date, end_date=subtask.task.end_date):
                    break

                subtask_filter: SubTask = session.query(SubTask).where(SubTask.description ==subtask.description,
                SubTask.due_date==date).first() or None
                subtask_filter.description = description
                subtasks.append(subtask_filter)
                date = DateUtil.get_next_week_date(date)

            for subtask_item in subtasks:
                if description:
                    try:
                        merged_subtask = session.merge(subtask_item)
                        session.commit()
                        session.refresh(merged_subtask)
                    except Exception as e:
                        session.rollback()
                        raise e
    @staticmethod
    def update_subtask(subtask: SubTask) -> SubTask:
        with create_session() as session:
            try:
                merged_subtask = session.merge(subtask)
                session.commit()
                session.refresh(merged_subtask)
                return merged_subtask
            except Exception as e:
                session.rollback()
                raise 
            
    @staticmethod
    def delete_subtask(subtask):
        with create_session() as session:
            if subtask:
                session.delete(subtask)
                session.commit()