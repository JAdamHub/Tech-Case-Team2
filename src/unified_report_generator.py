import os
import re
import glob
import json
from datetime import datetime
import sys
from dotenv import load_dotenv

# Definerer stien til mappe til rapporter
LLM_CHANGES_DIR = "_llm_changes"
FILES_TO_PROCESS_PATH = "files_to_process.txt"
REPORTS_DIR = "changes/reviews"

def get_files_to_process():
    """Læser listen af filer til behandling fra den angivne fil."""
    if not os.path.exists(FILES_TO_PROCESS_PATH):
        print(f"Advarsel: Filliste '{FILES_TO_PROCESS_PATH}' ikke fundet. Ingen filer at behandle.")
        return []
    try:
        with open(FILES_TO_PROCESS_PATH, 'r') as f:
            files = [line.strip() for line in f if line.strip()]
        if not files:
            print(f"Filliste '{FILES_TO_PROCESS_PATH}' er tom. Ingen filer at behandle.")
        return files
    except Exception as e:
        print(f"Fejl ved læsning af filliste fra {FILES_TO_PROCESS_PATH}: {e}")
        return []

def get_code_review_data(file_path):
    """Henter code review data for en given fil"""
    review_data = ""
    try:
        # Find den seneste review fil for dette filnavn
        basename = os.path.basename(file_path)
        reviews = sorted(glob.glob(f"{REPORTS_DIR}/*_{basename}"), reverse=True)
        
        if reviews:
            latest_review = reviews[0]
            with open(latest_review, 'r') as f:
                review_data = f.read()
            print(f"Fandt code review for {file_path}: {latest_review}")
            return review_data
        else:
            print(f"Ingen code review fundet for {file_path}")
            return None
    except Exception as e:
        print(f"Fejl ved hentning af code review for {file_path}: {e}")
        return None

def get_bug_fix_data(file_path):
    """Simulerer bug fix data for en given fil (gemmes normalt ikke som en fil)"""
    try:
        # Kør bug_fix_suggestions.py for at få data
        import subprocess
        
        # Vi gemmer output fra scriptet
        result = subprocess.run(
            [sys.executable, 'src/bug_fix_suggestions.py'],
            capture_output=True,
            text=True
        )
        
        # Filtrer output til kun at indeholde information om den specifikke fil
        lines = result.stdout.split('\n')
        file_bug_data = []
        capture = False
        
        for line in lines:
            if f"Analyzing {file_path}" in line:
                capture = True
                file_bug_data.append(line)
            elif capture and (line.startswith("Analyzing") or not line.strip()):
                capture = False
            elif capture:
                file_bug_data.append(line)
        
        if file_bug_data:
            return "\n".join(file_bug_data)
        else:
            print(f"Ingen bug fix data fundet for {file_path}")
            return "Ingen potentielle bugs fundet."
    except Exception as e:
        print(f"Fejl ved hentning af bug fix data for {file_path}: {e}")
        return "Fejl ved hentning af bug fix data."

def get_linting_data(file_path):
    """Henter linting data fra _llm_changes mappen"""
    try:
        # Normaliser filstien for match
        norm_path = file_path.replace('/', '_').replace('.', '_')
        
        # Find den seneste linting-rapport for denne fil
        reports = sorted(glob.glob(f"{LLM_CHANGES_DIR}/*_{norm_path}.md"), reverse=True)
        
        linting_reports = []
        for report in reports:
            with open(report, 'r') as f:
                content = f.read()
                # Kontroller om det er en linting-rapport
                if 'change_type: "Linting"' in content:
                    linting_reports.append((report, content))
        
        if linting_reports:
            report_path, content = linting_reports[0]  # Tag den seneste
            print(f"Fandt linting rapport for {file_path}: {report_path}")
            return content
        else:
            print(f"Ingen linting rapporter fundet for {file_path}")
            return None
    except Exception as e:
        print(f"Fejl ved hentning af linting data for {file_path}: {e}")
        return None

def get_test_data(file_path):
    """Henter test data fra _llm_changes mappen"""
    try:
        # Normaliser filstien for match
        norm_path = file_path.replace('/', '_').replace('.', '_')
        
        # Find den seneste test-rapport for denne fil
        reports = sorted(glob.glob(f"{LLM_CHANGES_DIR}/*_*{norm_path}*.md"), reverse=True)
        
        test_reports = []
        for report in reports:
            with open(report, 'r') as f:
                content = f.read()
                # Kontroller om det er en test-rapport
                if 'change_type: "Test Generation"' in content:
                    test_reports.append((report, content))
        
        if test_reports:
            report_path, content = test_reports[0]  # Tag den seneste
            print(f"Fandt test rapport for {file_path}: {report_path}")
            return content
        else:
            print(f"Ingen test rapporter fundet for {file_path}")
            return None
    except Exception as e:
        print(f"Fejl ved hentning af test data for {file_path}: {e}")
        return None

def generate_unified_report(file_path):
    """Genererer en samlet rapport for en fil baseret på alle scripts"""
    print(f"Genererer samlet rapport for {file_path}...")
    
    # Hent data fra alle forskellige scripts
    code_review_data = get_code_review_data(file_path)
    bug_fix_data = get_bug_fix_data(file_path)
    linting_data = get_linting_data(file_path)
    test_data = get_test_data(file_path)
    
    # Generer en timestamp til filnavnet
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Normaliser filnavnet til brug i rapportens filnavn
    norm_file_name = file_path.replace('/', '_').replace('.', '_')
    
    # Opret rapportfilnavn
    report_filename = f"{timestamp}_{norm_file_name}_unified.md"
    report_path = os.path.join(LLM_CHANGES_DIR, report_filename)
    
    # Sørg for at _llm_changes-mappen findes
    os.makedirs(LLM_CHANGES_DIR, exist_ok=True)
    
    # Opret Jekyll front matter
    front_matter = f"""---
layout: llm_change
title: "Samlet Rapport for {os.path.basename(file_path)}"
date: {datetime.now().isoformat()}
file: "{file_path}"
change_type: "Unified Report"
consolidated: true
---
"""
    
    # Byg rapportens indhold
    report_content = [front_matter]
    
    report_content.append(f"# Samlet Rapport for {file_path}\n")
    report_content.append(f"*Genereret: {datetime.now().strftime('%d-%m-%Y %H:%M')}*\n")
    
    # Tilføj code review sektion hvis tilgængelig
    if code_review_data:
        report_content.append("## Code Review\n")
        # Fjern eventuelle Jekyll front matter fra den oprindelige rapport
        content = re.sub(r"^---.*?---\n", "", code_review_data, flags=re.DOTALL)
        report_content.append(content)
        report_content.append("\n")
    
    # Tilføj bug fix sektion
    report_content.append("## Bug Fix Forslag\n")
    report_content.append("```\n")
    report_content.append(bug_fix_data)
    report_content.append("```\n")
    
    # Tilføj linting sektion hvis tilgængelig
    if linting_data:
        report_content.append("## Linting Fixes\n")
        # Fjern eventuelle Jekyll front matter fra den oprindelige rapport
        content = re.sub(r"^---.*?---\n", "", linting_data, flags=re.DOTALL)
        report_content.append(content)
        report_content.append("\n")
    
    # Tilføj test generation sektion hvis tilgængelig
    if test_data:
        report_content.append("## Automatisk Test Generation\n")
        # Fjern eventuelle Jekyll front matter fra den oprindelige rapport
        content = re.sub(r"^---.*?---\n", "", test_data, flags=re.DOTALL)
        report_content.append(content)
        report_content.append("\n")
    
    # Skriv den samlede rapport til en fil
    try:
        with open(report_path, 'w') as f:
            f.write("\n".join(report_content))
        print(f"Samlet rapport gemt: {report_path}")
        
        # Opdater indeksfilen
        update_index_with_category(f"Samlet Rapport for {os.path.basename(file_path)}", 
                                  os.path.basename(report_path), 
                                  "Unified Report", 
                                  datetime.now())
        
        return report_path
    except Exception as e:
        print(f"Fejl ved lagring af samlet rapport {report_path}: {e}")
        return None

def update_index_with_category(title, report_filename, change_type, timestamp):
    """Opdaterer indeksfilen med kategoriserede ændringsoplysninger"""
    try:
        index_path = os.path.join(LLM_CHANGES_DIR, "index.md")
        
        # Opret indeksfil, hvis den ikke findes
        if not os.path.exists(index_path):
            with open(index_path, 'w') as idx:
                idx.write("---\nlayout: page\ntitle: LLM-genererede Ændringer\n---\n\n")
                idx.write("# LLM-genererede Ændringer\n\n")
                idx.write("Dette er en oversigt over alle ændringer foretaget af LLM (Large Language Model) i dette projekt.\n\n")
                idx.write("## Seneste Ændringer\n\n")
                idx.write("Følgende ændringer er blevet genereret af LLM:\n\n")
                idx.write("<!-- Automatisk opdateret af LLM scripts -->")
        
        # Tilføj den nye ændringspost med dato og kategorioplysninger
        with open(index_path, 'a') as idx:
            idx.write(f"\n- [{title}](./{report_filename}) <small>[{change_type}] {timestamp.strftime('%d-%m-%Y %H:%M')}</small>")
            
    except Exception as e:
        print(f"Fejl ved opdatering af indeks med kategori: {e}")

def remove_duplicate_reports():
    """Fjerner delvise/ældre rapporter efter at den samlede rapport er genereret"""
    files_processed = set()
    
    try:
        # Find alle samlede rapporter først
        unified_reports = []
        for report in glob.glob(f"{LLM_CHANGES_DIR}/*_unified.md"):
            with open(report, 'r') as f:
                content = f.read()
                match = re.search(r'file: "(.*?)"', content)
                if match:
                    file_path = match.group(1)
                    files_processed.add(file_path)
                    unified_reports.append((file_path, report))
        
        # Fjern alle ikke-samlede rapporter for filer, der har en samlet rapport
        for report in glob.glob(f"{LLM_CHANGES_DIR}/*.md"):
            if "_unified.md" in report or "index.md" in report:
                continue
                
            with open(report, 'r') as f:
                content = f.read()
                match = re.search(r'file: "(.*?)"', content)
                if match:
                    file_path = match.group(1)
                    if file_path in files_processed:
                        print(f"Fjerner delvis rapport, da samlet rapport findes: {report}")
                        os.remove(report)
    except Exception as e:
        print(f"Fejl ved fjernelse af duplikate rapporter: {e}")

def generate_unified_reports():
    """Hovedfunktion for at generere samlede rapporter for alle filer"""
    print('Genererer samlede rapporter for alle filer...')
    
    # Hent filer til behandling fra listefilen
    files_to_process = get_files_to_process()
    
    if not files_to_process:
        print("Ingen filer angivet til rapportgenerering.")
        return
    
    for file_path in files_to_process:
        # Generer samlet rapport for hver fil
        generate_unified_report(file_path)
    
    # Ryd op i delvise rapporter
    remove_duplicate_reports()
    
    print("\n--- Samlet Rapportgenerering Fuldført ---")

if __name__ == '__main__':
    generate_unified_reports()
