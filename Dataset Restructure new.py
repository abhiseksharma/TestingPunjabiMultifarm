import os
import shutil
from rdflib import Graph

# ============================================================
# INPUT STRUCTURE
#
# dataset/
# ├── ont/
# │   ├── hi/
# │   │   ├── cmt-hi.owl
# │   │   ├── conference-hi.owl
# │   │   └── ...
# │   ├── en/
# │   │   ├── conference-en.owl
# │   │   └── ...
# │   └── ...
# │
# └── ref/
#     ├── hi-en/
#     │   ├── cmt-conference-hi-en.rdf
#     │   └── ...
#     └── ...
#
#
# OUTPUT STRUCTURE
#
# my-track/
# ├── testcase1/
# │   ├── source.rdf
# │   ├── target.rdf
# │   ├── reference.rdf
# │
# ├── testcase2/
# │   ├── source.rdf
# │   ├── target.rdf
# │   ├── reference.rdf
# │
# └── ...
# ============================================================

# =========================
# PATHS
# =========================

dataset_path = "dataset-2015-open/dataset-2015-testing"

ont_folder = os.path.join(dataset_path, "ont")
ref_folder = os.path.join(dataset_path, "ref")

output_folder = "Dataset with punjabi rdf"

os.makedirs(output_folder, exist_ok=True)

# =========================
# FUNCTION:
# CONVERT OWL -> RDF/XML
# =========================

def convert_owl_to_rdf(input_owl, output_rdf):

    g = Graph()

    try:
        g.parse(input_owl)

        # Save as RDF/XML
        g.serialize(
            destination=output_rdf,
            format="xml"
        )

    except Exception as e:
        print(f"\nError converting:")
        print(input_owl)
        print(e)

# =========================
# TESTCASE COUNTER
# =========================

testcase_counter = 1

# =========================
# PROCESS REFERENCE FILES
# =========================

for lang_folder in os.listdir(ref_folder):

    lang_folder_path = os.path.join(ref_folder, lang_folder)

    if not os.path.isdir(lang_folder_path):
        continue

    print(f"\nProcessing folder: {lang_folder}")

    for rdf_file in os.listdir(lang_folder_path):

        if not rdf_file.endswith(".rdf"):
            continue

        rdf_path = os.path.join(lang_folder_path, rdf_file)

        # Example:
        # cmt-conference-hi-en.rdf

        base_name = rdf_file.replace(".rdf", "")

        parts = base_name.split("-")

        # ===================================================
        # VALIDATE FILE NAME
        # ===================================================

        if len(parts) < 4:
            print(f"Skipping invalid file: {rdf_file}")
            continue

        source_ontology = parts[0]
        target_ontology = parts[1]

        source_lang = parts[-2]
        target_lang = parts[-1]

        # ===================================================
        # FIND OWL FILES
        # ===================================================

        source_owl_name = f"{source_ontology}-{source_lang}.owl"
        target_owl_name = f"{target_ontology}-{target_lang}.owl"

        source_owl_path = os.path.join(
            ont_folder,
            source_lang,
            source_owl_name
        )

        target_owl_path = os.path.join(
            ont_folder,
            target_lang,
            target_owl_name
        )

        # ===================================================
        # CREATE TESTCASE FOLDER
        # ===================================================

        testcase_folder = os.path.join(
            output_folder,
            f"testcase{testcase_counter}"
        )

        os.makedirs(testcase_folder, exist_ok=True)

        # ===================================================
        # OUTPUT FILE PATHS
        # ===================================================

        source_output = os.path.join(
            testcase_folder,
            "source.rdf"
        )

        target_output = os.path.join(
            testcase_folder,
            "target.rdf"
        )

        reference_output = os.path.join(
            testcase_folder,
            "reference.rdf"
        )

        # ===================================================
        # CONVERT SOURCE
        # ===================================================

        if os.path.exists(source_owl_path):

            convert_owl_to_rdf(
                source_owl_path,
                source_output
            )

        else:
            print(f"Missing source OWL:")
            print(source_owl_path)
            continue

        # ===================================================
        # CONVERT TARGET
        # ===================================================

        if os.path.exists(target_owl_path):

            convert_owl_to_rdf(
                target_owl_path,
                target_output
            )

        else:
            print(f"Missing target OWL:")
            print(target_owl_path)
            continue

        # ===================================================
        # COPY REFERENCE RDF
        # ===================================================

        shutil.copy(
            rdf_path,
            reference_output
        )

        print(f"Created testcase{testcase_counter}")

        testcase_counter += 1

print("\nAll testcases created successfully.")