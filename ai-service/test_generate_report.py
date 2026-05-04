import time
import requests

BASE_URL = "http://localhost:5000"

SAMPLE_SURVEY_DATA = """
Survey responses from 47 employees across 5 departments:

1. Leadership: Our senior management never discusses risk in meetings.
   The board risk committee meets quarterly but decisions are never made.

2. Risk Awareness: Most staff do not know what the risk register is.
   Only 3 out of 47 respondents could name our top operational risks.

3. Incident Reporting: Staff are afraid to report near misses.
   Two incidents went unreported last quarter due to fear of blame.

4. Training: Risk training was last updated in 2019.
   New joiners receive no risk management onboarding.

5. Accountability: Risk owners never update their assigned risks.
   No consequences exist for missing risk action deadlines.

Overall risk culture score: 2.1 out of 5.0
Survey completion rate: 78%
"""

def poll_job(job_id: str, max_wait: int = 60) -> dict:
    """
    Poll job status until complete or timeout.
    Returns final job response.
    """
    print(f"   Polling job {job_id[:8]}...")
    waited = 0

    while waited < max_wait:
        time.sleep(2)
        waited += 2

        r    = requests.get(
            f"{BASE_URL}/generate-report/{job_id}",
            timeout=10
        )
        data = r.json()
        status = data.get("status")
        print(f"   [{waited}s] Status: {status}")

        if status in ["complete", "failed"]:
            return data

    return {"status": "timeout", "error": "Job did not complete in time"}

def run_tests():
    print("=" * 60)
    print("Testing POST /generate-report — Async Pipeline")
    print("=" * 60)

    passed = 0
    failed = 0

    # Test 1: Returns job_id immediately
    print("\nTest 1: POST /generate-report returns job_id immediately")
    try:
        start = time.time()
        r     = requests.post(
            f"{BASE_URL}/generate-report",
            json={"survey_data": SAMPLE_SURVEY_DATA},
            timeout=10
        )
        elapsed = time.time() - start
        data    = r.json()

        print(f"Status  : {r.status_code}")
        print(f"Time    : {round(elapsed * 1000)}ms")
        print(f"job_id  : {data.get('job_id', '')[:8]}...")
        print(f"status  : {data.get('status')}")
        print(f"message : {data.get('message')}")

        if (
            r.status_code == 202 and
            data.get("job_id") and
            data.get("status") == "pending" and
            elapsed < 3.0
        ):
            print("PASSED ✓ — job_id returned immediately")
            passed += 1
            job_id_1 = data["job_id"]
        else:
            print("FAILED ✗")
            failed += 1
            job_id_1 = None

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1
        job_id_1 = None

    # Test 2: Poll until complete
    print("\nTest 2: Poll job until complete — expect full report")
    if not job_id_1:
        print("SKIPPED — no job_id from Test 1")
        failed += 1
    else:
        try:
            final = poll_job(job_id_1, max_wait=90)
            print(f"Final status : {final.get('status')}")

            if final.get("status") == "complete":
                report = final.get("result", {}).get("report", {})
                print(f"Title        : {report.get('title', '')[:60]}")
                print(f"Exec summary : {report.get('executive_summary', '')[:80]}...")
                print(f"Top items    : {len(report.get('top_items', []))}")
                print(f"Recs         : {len(report.get('recommendations', []))}")

                if (
                    report.get("title") and
                    report.get("executive_summary") and
                    report.get("overview") and
                    len(report.get("top_items", [])) >= 1 and
                    len(report.get("recommendations", [])) >= 1
                ):
                    print("PASSED ✓ — complete report generated")
                    passed += 1
                else:
                    print("FAILED ✗ — report missing required fields")
                    failed += 1
            else:
                print(f"FAILED ✗ — job ended with: {final.get('status')}")
                failed += 1

        except Exception as e:
            print(f"ERROR: {e}")
            failed += 1

    # Test 3: GET /generate-report/jobs lists all jobs
    print("\nTest 3: GET /generate-report/jobs shows job stats")
    try:
        r    = requests.get(
            f"{BASE_URL}/generate-report/jobs",
            timeout=10
        )
        data = r.json()

        print(f"Status  : {r.status_code}")
        stats = data.get("stats", {})
        print(f"Total   : {stats.get('total')}")
        print(f"Complete: {stats.get('complete')}")
        print(f"Failed  : {stats.get('failed')}")
        print(f"Jobs    : {len(data.get('jobs', []))}")

        if r.status_code == 200 and stats.get("total", 0) > 0:
            print("PASSED ✓ — jobs list working")
            passed += 1
        else:
            print("FAILED ✗")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 4: Invalid input returns 400
    print("\nTest 4: Empty survey_data — expect 400")
    try:
        r    = requests.post(
            f"{BASE_URL}/generate-report",
            json={"survey_data": ""},
            timeout=10
        )
        data = r.json()
        print(f"Status : {r.status_code}")
        print(f"Error  : {data.get('error')}")

        if r.status_code == 400:
            print("PASSED ✓ — validation working")
            passed += 1
        else:
            print("FAILED ✗")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 5: Job not found returns 404
    print("\nTest 5: Invalid job_id — expect 404")
    try:
        r    = requests.get(
            f"{BASE_URL}/generate-report/invalid-job-id-123",
            timeout=10
        )
        data = r.json()
        print(f"Status : {r.status_code}")
        print(f"Error  : {data.get('error')}")

        if r.status_code == 404:
            print("PASSED ✓ — 404 returned correctly")
            passed += 1
        else:
            print("FAILED ✗")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Summary 
    print("\n" + "=" * 60)
    print(f"Results      : {passed} passed, {failed} failed")
    print(f"Day 11 status: {'COMPLETE ✓' if failed == 0 else 'FAILED ✗'}")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()