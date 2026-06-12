"""CLI entrypoint for the background worker."""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from app.config import get_settings
from app.db.session import get_sessionmaker
from app.worker.runner import WorkerRunner


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Internal Sea background worker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    once_parser = subparsers.add_parser("run-once", help="Process one worker batch and exit")
    once_parser.add_argument("--batch-size", type=int, default=None)
    once_parser.add_argument("--instance-id", type=str, default=None)

    loop_parser = subparsers.add_parser("run-loop", help="Run worker continuously")
    loop_parser.add_argument("--interval", type=int, default=None, help="Poll interval in seconds")
    loop_parser.add_argument("--batch-size", type=int, default=None)
    loop_parser.add_argument("--instance-id", type=str, default=None)

    return parser


async def _run_once(*, batch_size: int | None, instance_id: str | None) -> int:
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        runner = WorkerRunner(session, instance_id=instance_id, batch_size=batch_size)
        result = await runner.run_once()
        print(result.summary)
        if result.failures:
            for failure in result.failures:
                print(f"  failure: {failure}", file=sys.stderr)
        return 0


async def _run_loop(
    *,
    interval: int | None,
    batch_size: int | None,
    instance_id: str | None,
) -> int:
    sessionmaker = get_sessionmaker()
    await WorkerRunner.run_loop_with_session_factory(
        sessionmaker,
        instance_id=instance_id,
        batch_size=batch_size,
        interval_seconds=interval,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=get_settings().log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "run-once":
            return asyncio.run(
                _run_once(batch_size=args.batch_size, instance_id=args.instance_id)
            )
        if args.command == "run-loop":
            return asyncio.run(
                _run_loop(
                    interval=args.interval,
                    batch_size=args.batch_size,
                    instance_id=args.instance_id,
                )
            )
    except KeyboardInterrupt:
        return 0
    except Exception:
        logging.exception("Worker fatal error")
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
