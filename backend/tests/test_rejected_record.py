from sqlmodel import Session, select
from app.database import engine
from app.models.IngestionRun import IngestionRun
from app.models.RejectedRecord import RejectedRecord
from app.ingestion.telemetry_processor import parse_rad_row


malformed_row = "this is a deliberately malformed row"

with Session(engine) as session:
    run = IngestionRun(
        source_url="test://rejected-record",
        status="running",
    )
    session.add(run)
    session.commit()
    session.refresh(run)

    run_id = run.id

    try:
        parse_rad_row(malformed_row)

    except (ValueError, TypeError, IndexError) as exc:
        session.add(
            RejectedRecord(
                ingestion_run_id=run_id,
                source_row_number=1,
                raw_row=malformed_row,
                reason=str(exc)[:500],
            )
        )

        run.rejected_count = 1
        run.status = "completed"
        session.add(run)
        session.commit()

        print("Test run:", run_id)
        print("Status:", run.status)
        print("Rejected count:", run.rejected_count)
        print("Reason:", str(exc))

    else:
        run.status = "failed"
        session.add(run)
        session.commit()
        raise AssertionError("Malformed row was unexpectedly accepted")

with Session(engine) as session:
    saved = session.get(IngestionRun, run_id)
    rejected = session.exec(
    select(RejectedRecord).where(
        RejectedRecord.ingestion_run_id == run_id
    )
).all()

    print("Saved rejection records:", len(rejected))
    print("Saved run status:", saved.status)