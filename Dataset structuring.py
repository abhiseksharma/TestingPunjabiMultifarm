import os
import shutil
from rdflib import Graph

# ============================================================
# UPDATED DATASET STRUCTURE
#
# dataset/
# ├── ont/
# │   ├── ar/
# │   │   ├── cmt-ar.owl
# │   │   ├── conference-ar.owl
# │   │   └── ...
# │   │
# │   ├── hi/
# │   │   ├── cmt-hi.owl
# │   │   ├── conference-hi.owl
# │   │   └── ...
# │   │
# │   └── ...
# │
# └── ref/
#     ├── hi-en/
#     │   ├── cmt-conference-hi-en.rdf
#     │   └── ...
#     └── ...
#
#
# OUTPUT:
#
# output/
# ├── cmt-conference-hi-en/
# │   └── component/
# │       ├── source.xml
# │       ├── target.xml
# │       └── reference.xml
# │
# └── ...
# ============================================================

# =========================
# PATHS
# =========================

dataset_path = "dataset-2015-open/dataset-2015-testing"

ont_folder = os.path.join(dataset_path, "ont")
ref_folder = os.path.join(dataset_path, "ref")

output_folder = "Dataset with punjabi"

os.makedirs(output_folder, exist_ok=True)

# =========================
# FUNCTION:
# OWL -> XML
# =========================

def convert_owl_to_xml(input_owl, output_xml):

    g = Graph()

    try:
        g.parse(input_owl)

        g.serialize(
            destination=output_xml,
            format="xml"
        )

    except Exception as e:
        print(f"\nError converting:")
        print(input_owl)
        print(e)

# =========================
# PROCESS REF FOLDERS
# =========================

for lang_folder in os.listdir(ref_folder):

    lang_folder_path = os.path.join(ref_folder, lang_folder)

    if not os.path.isdir(lang_folder_path):
        continue

    print(f"\nProcessing language pair folder: {lang_folder}")

    # Example:
    # hi-en

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

        # NEW STRUCTURE:
        # ont/hi/cmt-hi.owl

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
        # CREATE OUTPUT STRUCTURE
        # ===================================================

        pair_output_folder = os.path.join(
            output_folder,
            base_name
        )

        component_folder = os.path.join(
            pair_output_folder,
            "component"
        )

        os.makedirs(component_folder, exist_ok=True)

        # ===================================================
        # OUTPUT FILES
        # ===================================================

        source_xml_path = os.path.join(
            component_folder,
            "source.xml"
        )

        target_xml_path = os.path.join(
            component_folder,
            "target.xml"
        )

        reference_xml_path = os.path.join(
            component_folder,
            "reference.xml"
        )

        # ===================================================
        # CONVERT SOURCE OWL
        # ===================================================

        if os.path.exists(source_owl_path):

            convert_owl_to_xml(
                source_owl_path,
                source_xml_path
            )

        else:
            print(f"Missing source OWL:")
            print(source_owl_path)

        # ===================================================
        # CONVERT TARGET OWL
        # ===================================================

        if os.path.exists(target_owl_path):

            convert_owl_to_xml(
                target_owl_path,
                target_xml_path
            )

        else:
            print(f"Missing target OWL:")
            print(target_owl_path)

        # ===================================================
        # COPY RDF AS reference.xml
        # ===================================================

        shutil.copy(
            rdf_path,
            reference_xml_path
        )

        print(f"Created: {base_name}")

print("\nAll files processed successfully.")