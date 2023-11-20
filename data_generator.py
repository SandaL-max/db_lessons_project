"""Generator of data for db"""
from faker import Faker
from models.worker import Worker
from models.project import Project
from models.order import Order

fake = Faker()


async def generate_worker():
    """Generate one worker"""
    worker = fake.simple_profile()
    worker["post"] = fake.job()
    worker["salary"] = fake.random_int(min=30000, max=100000)
    return Worker(
        full_name=worker["name"],
        post=worker["post"],
        salary=worker["salary"],
        details=worker,
    )


async def generate_workers(quantity: int):
    """Generate several workers"""
    return [await generate_worker() for i in range(quantity)]


async def generate_project():
    """Generate one project"""
    return Project(
        name=fake.catch_phrase(),
        description=fake.text(),
        end_date=fake.date_between(start_date="+30d", end_date="+1y"),
        complexity_level=fake.random_int(min=1, max=10),
    )


async def generate_projects(quantity: int):
    """Generate several projects"""
    return [await generate_project() for i in range(quantity)]


async def generate_order(project_id_range: tuple, worker_id_range: tuple):
    """Generate one order"""
    return Order(
        name=fake.company(),
        description=fake.text(),
        start_date=fake.date_between(start_date="+1d", end_date="+2m"),
        deadline_date=fake.date_between(start_date="+3m", end_date="+1y"),
        real_end_date=fake.date_between(start_date="+1y", end_date="+2y"),
        complexity_level=fake.random_int(min=1, max=10),
        project_id=fake.random_int(min=project_id_range[0], max=project_id_range[1]),
        worker_id=fake.random_int(min=worker_id_range[0], max=worker_id_range[1]),
    )


async def generate_orders(
    quantity: int, project_id_range: tuple, worker_id_range: tuple
):
    """Generate several orders"""
    return [
        await generate_order(project_id_range, worker_id_range) for i in range(quantity)
    ]
