import time, argparse
from agent.core_agent import CoreAgent
from tools.log_streamer import LogStreamer
from utils.logger import AuditLogger

def main(run_time=10, interval=1.0):
    logger = AuditLogger('main')
    agent = CoreAgent()
    streamer = LogStreamer()
    logger.log('system_start', {'run_time': run_time, 'interval': interval})
    print('[INFO] Incident Insight Agent started. Listening for incidents... (Ctrl+C to stop)')
    start = time.time()
    try:
        while True:
            ev = streamer.next_event()
            print('\n[Incident Detected] ', ev['title'])
            # Agent handles event
            result = agent.handle_event(ev)
            print('[Decision] ', result['action'])
            logger.log('incident_processed', {'incident': ev['id'], 'decision': result})
            time.sleep(interval)
            if run_time and (time.time() - start) > run_time:
                break
    except KeyboardInterrupt:
        print('\n[INFO] Interrupted by user. Exiting.')
    logger.log('system_end', {'status': 'finished'})
    print('[INFO] Run complete. Audit saved to logs/audit.log')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Incident Insight Agent CLI')
    parser.add_argument('--run-time', type=int, default=20, help='Total run time in seconds (default 20)')
    parser.add_argument('--interval', type=float, default=1.0, help='Interval between events in seconds (default 1.0)')
    args = parser.parse_args()
    main(run_time=args.run_time, interval=args.interval)
