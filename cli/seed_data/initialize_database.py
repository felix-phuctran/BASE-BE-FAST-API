import asyncio

from dependencies.session import AsyncSessionLocal
from services.implement.cli_service_impl import CliServiceImpl


async def run_cli():
    # 1️⃣ Create database session
    async with AsyncSessionLocal() as db:
        # 2️⃣ Initialize CLI service
        cli_service = CliServiceImpl(db)

        # 3️⃣ Chạy từng bước và log kết quả
        print("⏳ Initializing DB...")
        db_result = await cli_service._initialize_db()
        print(f"✅ Database Init Result: {db_result}")

        print("⏳ Initializing User...")
        user_result = await cli_service._initialize_user(db)
        print(f"✅ User Init Result: {user_result}")


if __name__ == "__main__":
    asyncio.run(run_cli())  # ✅ Chạy coroutine chính xác
