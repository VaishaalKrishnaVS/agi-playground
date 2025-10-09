from agents import analyst_agent, researcher_agent, writer_agent
import logging
import time

# Get the same logger as agents.py
log = logging.getLogger(__name__)


def process(user_input: str):
    workflow_start_time = time.time()

    log.info(f"🎯 WORKFLOW STARTED: {user_input}")

    print(f"\nProcessing: '{user_input}'")

    # STEP 1: RESEARCH PHASE
    step1_start = time.time()
    log.info(f"🔍 STEP 1: Research Phase Starting")
    print("\nStep 1: Researcher Agent gathering web information...")

    research_prompt = (
        f"Research: '{user_input}'. Use your available tools to gather information from reliable sources. "
        f"Focus on being concise and thorough, but limit web requests to 1-2 sources."
    )

    researcher_response = researcher_agent(research_prompt)
    research_findings = str(researcher_response)
    step1_time = time.time() - step1_start

    log.info(f"✅ Research Complete ({step1_time:.1f}s)")

    print("Research complete")
    print("Passing research findings to Analyst Agent...\n")

    # STEP 2: ANALYSIS PHASE
    step2_start = time.time()
    log.info(f"🧠 STEP 2: Analysis Phase Starting")
    print("Step 2: Analyst Agent analyzing findings...")

    analysis_prompt = (
        f"Analyze these findings about '{user_input}':\n\n{research_findings}"
    )

    analyst_response = analyst_agent(analysis_prompt)
    analysis = str(analyst_response)
    step2_time = time.time() - step2_start

    log.info(f"✅ Analysis Complete ({step2_time:.1f}s)")

    print("Analysis complete")
    print("Passing analysis to Writer Agent...\n")

    # STEP 3: WRITING PHASE
    step3_start = time.time()
    log.info(f"✍️ STEP 3: Writing Phase Starting")
    print("Step 3: Writer Agent creating final report...")

    writing_prompt = (
        f"Create a report on '{user_input}' based on this analysis:\n\n{analysis}"
    )

    final_report = writer_agent(writing_prompt)
    step3_time = time.time() - step3_start

    log.info(f"✅ Writing Complete ({step3_time:.1f}s)")

    print("Report creation complete")

    # WORKFLOW SUMMARY
    total_workflow_time = time.time() - workflow_start_time
    log.info(
        f"🏁 Workflow Complete - Total: {total_workflow_time:.1f}s (Research: {step1_time:.1f}s, Analysis: {step2_time:.1f}s, Writing: {step3_time:.1f}s)"
    )

    return final_report


if __name__ == "__main__":
    log.info(f"🎬 Application Started")

    print("\nAgentic Workflow: Research Assistant\n")
    print("Try research questions or fact-check claims.\n")

    session_start = time.time()
    query_count = 0

    while True:
        try:
            user_input = input("\n ")
            if user_input.lower() == "exit":
                session_duration = time.time() - session_start
                log.info(
                    f"🛑 Session End - {query_count} queries in {session_duration:.1f}s"
                )
                print("Closing ")
                break

            query_count += 1
            log.info(f"📥 Query #{query_count}: {user_input}")

            final_report = process(user_input=user_input)

        except KeyboardInterrupt:
            session_duration = time.time() - session_start
            log.info(
                f"⚠️ Interrupted - {query_count} queries in {session_duration:.1f}s"
            )
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            log.error(f"❌ Error in Query #{query_count}: {str(e)}")
            print(f"\nAn error occurred: {str(e)}")
            print("Please try a different request.")
