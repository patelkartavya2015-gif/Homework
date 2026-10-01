import colorama
from colorama import Fore, Style
from textblob import TextBlob
import json
import csv
import random
from datetime import datetime

# Initialize colorama with autoreset
colorama.init(autoreset=True)

# Agent Rank System based on total entries
RANKS = [
    (0, "Recruit Spy"),
    (5, "Field Operative"),
    (15, "Special Agent"),
    (30, "Senior Intelligence Officer"),
    (50, "Master Spy Commander")
]

def get_agent_rank(count):
    current_rank = "Recruit Spy"
    for threshold, rank in RANKS:
        if count >= threshold:
            current_rank = rank
    return current_rank

def print_banner():
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║             🐍 SENTIMENT SPY v3.0: OMEGA 🐍                ║")
    print("║     Advanced Covert Emotional Intelligence Analyzer        ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")

def get_sentiment_details(polarity):
    if polarity > 0.25:
        return "Positive", Fore.GREEN, "😃"
    elif polarity < -0.25:
        return "Negative", Fore.RED, "😢"
    else:
        return "Neutral", Fore.YELLOW, "😑"

def display_help():
    print(f"\n{Fore.CYAN}--- CLASSIFIED AGENT COMMAND MENU ---{Style.RESET_ALL}")
    print(f"  • {Fore.YELLOW}history{Style.RESET_ALL}        - View all recorded intelligence logs")
    print(f"  • {Fore.YELLOW}stats{Style.RESET_ALL}          - View comprehensive emotional analytics & trends")
    print(f"  • {Fore.YELLOW}search {Style.RESET_ALL}  - Search intelligence logs for specific text")
    print(f"  • {Fore.YELLOW}export json{Style.RESET_ALL}    - Export formatted logs to JSON format")
    print(f"  • {Fore.YELLOW}export csv{Style.RESET_ALL}     - Export data to a secure CSV report")
    print(f"  • {Fore.YELLOW}quote{Style.RESET_ALL}          - Receive tactical spy inspiration or advice")
    print(f"  • {Fore.YELLOW}profile{Style.RESET_ALL}        - View your operative profile & clearance rank")
    print(f"  • {Fore.YELLOW}reset{Style.RESET_ALL}          - Wipe current session intelligence memory")
    print(f"  • {Fore.YELLOW}help{Style.RESET_ALL}           - Display this tactical help manual")
    print(f"  • {Fore.YELLOW}exit{Style.RESET_ALL}           - Terminate secure connection\n")

def display_quote():
    quotes = [
        "\"The eyes and ears of an agent are the shield of the nation.\" - Unknown",
        "\"Emotions are data. Analyze them before they analyze you.\" - Director X",
        "\"A calm mind in a storm of chaos is a spy's best weapon.\" - Cipher 9",
        "\"Trust but verify, especially your own sentiment frequency.\" - Agent Zero"
    ]
    print(f"\n{Fore.MAGENTA}[TACTICAL INTEL] {Style.BRIGHT}{random.choice(quotes)}{Style.RESET_ALL}\n")

def main():
    print_banner()
    
    # Agent Authentication
    user_name = input(f"{Fore.MAGENTA}Please enter your agent codename: {Style.RESET_ALL}").strip()
    if not user_name:
        user_name = "Ghost Operative"
    
    print(f"\n{Fore.CYAN}Secure connection established. Welcome back, Agent {user_name}! 🕵️‍♂️")
    print(f"Type {Fore.YELLOW}help{Style.RESET_ALL} to view tactical commands or start typing sentences for analysis.\n")

    conversation_history = []

    while True:
        try:
            user_input = input(f"{Fore.RED}SpyNet [{user_name}] > {Style.RESET_ALL}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Fore.YELLOW}[!] Emergency protocol invoked. Terminating session, Agent {user_name}.")
            break

        # 1. Handle Empty Input
        if not user_input:
            print(f"{Fore.RED}[x] Security Alert: Blank transmission rejected. Enter valid intel text.{Style.RESET_ALL}")
            continue

        parts = user_input.split(" ", 1)
        command = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        # 2. Command Processing
        if command == "exit":
            print(f"\n{Fore.CYAN}Mission session closed. Stay safe out in the field, Agent {user_name}! 🚀{Style.RESET_ALL}")
            break

        elif command == "help":
            display_help()
            continue

        elif command == "quote":
            display_quote()
            continue

        elif command == "profile":
            total_logs = len(conversation_history)
            rank = get_agent_rank(total_logs)
            print(f"\n{Fore.CYAN}--- OPERATIVE DOSSIER ---{Style.RESET_ALL}")
            print(f"  • Codename:       {Fore.MAGENTA}{user_name}{Style.RESET_ALL}")
            print(f"  • Clearance Rank: {Fore.GREEN}{rank}{Style.RESET_ALL}")
            print(f"  • Log Entries:    {total_logs}")
            print(f"  • Encryption:     AES-256 (Simulated)\n")
            continue

        elif command == "reset":
            confirm = input(f"{Fore.YELLOW}⚠️ WARNING: Purge all session intel memory? (y/n): {Style.RESET_ALL}").lower()
            if confirm == 'y':
                conversation_history.clear()
                print(f"{Fore.GREEN}[✓] Intelligence history securely wiped from buffer memory.{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.BLUE}[i] Purge request aborted.{Style.RESET_ALL}\n")
            continue

        elif command == "history":
            if not conversation_history:
                print(f"{Fore.YELLOW}[i] No logs recorded in current session buffer.{Style.RESET_ALL}\n")
            else:
                print(f"\n{Fore.CYAN}--- CLASSIFIED LOGS ARCHIVE ({len(conversation_history)}) ---{Style.RESET_ALL}")
                for idx, (text, polarity, sentiment_type) in enumerate(conversation_history, start=1):
                    _, color, emoji = get_sentiment_details(polarity)
                    print(f"  {idx}. {color}{emoji} [{sentiment_type}] \"{text}\" (Polarity: {polarity:.2f})")
                print()
            continue

        elif command == "search":
            if not arg:
                print(f"{Fore.RED}[x] Usage error: Type 'search ' to query intelligence logs.{Style.RESET_ALL}\n")
                continue
            matches = [(idx, t, p, s) for idx, (t, p, s) in enumerate(conversation_history, start=1) if arg.lower() in t.lower()]
            if not matches:
                print(f"{Fore.YELLOW}[i] No intelligence logs found matching keyword: '{arg}'{Style.RESET_ALL}\n")
            else:
                print(f"\n{Fore.CYAN}--- SEARCH RESULTS FOR '{arg}' ({len(matches)}) ---{Style.RESET_ALL}")
                for idx, text, polarity, sentiment_type in matches:
                    _, color, emoji = get_sentiment_details(polarity)
                    print(f"  {idx}. {color}{emoji} [{sentiment_type}] \"{text}\" (Polarity: {polarity:.2f})")
                print()
            continue

        elif command == "export":
            if not conversation_history:
                print(f"{Fore.YELLOW}[i] No data available for export.{Style.RESET_ALL}\n")
                continue
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if arg == "json":
                filename = f"sentiment_intel_{timestamp}.json"
                export_data = [{"text": t, "polarity": p, "sentiment": s} for t, p, s in conversation_history]
                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(export_data, f, indent=4)
                    print(f"{Fore.GREEN}[✓] Encrypted JSON report successfully saved as {filename}{Style.RESET_ALL}\n")
                except Exception as e:
                    print(f"{Fore.RED}[x] JSON Export failed: {e}{Style.RESET_ALL}\n")
            elif arg == "csv":
                filename = f"sentiment_intel_{timestamp}.csv"
                try:
                    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["Text", "Polarity", "Sentiment"])
                        for t, p, s in conversation_history:
                            writer.writerow([t, p, s])
                    print(f"{Fore.GREEN}[✓] Secure CSV report successfully saved as {filename}{Style.RESET_ALL}\n")
                except Exception as e:
                    print(f"{Fore.RED}[x] CSV Export failed: {e}{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}[x] Unknown export format. Use 'export json' or 'export csv'.{Style.RESET_ALL}\n")
            continue

        elif command == "stats":
            if not conversation_history:
                print(f"{Fore.YELLOW}[i] Insufficient data for statistical intel report.{Style.RESET_ALL}\n")
            else:
                total = len(conversation_history)
                pos_count = sum(1 for _, _, st in conversation_history if st == "Positive")
                neg_count = sum(1 for _, _, st in conversation_history if st == "Negative")
                neu_count = sum(1 for _, _, st in conversation_history if st == "Neutral")
                avg_polarity = sum(p for _, p, _ in conversation_history) / total
                _, avg_color, avg_emoji = get_sentiment_details(avg_polarity)

                print(f"\n{Fore.CYAN}--- TACTICAL EMOTIONAL ANALYTICS ---{Style.RESET_ALL}")
                print(f"  • Total Transmissions:   {total}")
                print(f"  • Positive Frequency:    {Fore.GREEN}{pos_count} ({pos_count/total*100:.1f}%){Style.RESET_ALL}")
                print(f"  • Negative Frequency:    {Fore.RED}{neg_count} ({neg_count/total*100:.1f}%){Style.RESET_ALL}")
                print(f"  • Neutral Frequency:     {Fore.YELLOW}{neu_count} ({neu_count/total*100:.1f}%){Style.RESET_ALL}")
                print(f"  • Mean Polarity Index:   {avg_color}{avg_emoji} {avg_polarity:.2f}{Style.RESET_ALL}")
                print(f"  • Operative Rank:        {Fore.MAGENTA}{get_agent_rank(total)}{Style.RESET_ALL}\n")
            continue

        # 3. Sentiment Analysis Execution for Regular Sentences
        polarity = TextBlob(user_input).sentiment.polarity
        sentiment_type, color, emoji = get_sentiment_details(polarity)

        # Append to secure memory buffer
        conversation_history.append((user_input, polarity, sentiment_type))

        print(f"{color}{emoji} Intelligence Analyzed: {sentiment_type} | Polarity Score: {polarity:.2f}\n")

if __name__ == "__main__":
    main()