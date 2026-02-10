import os

def run_all_training():
    print(">>> STARTING FULL TRAINING PIPELINE <<<")
    
    # Run from root of urbanflux_ai
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)

    print("\n--- 1. Generating Data ---")
    if os.system("python training/generate_data.py") != 0:
        print("Error in data generation")
        return
    
    print("\n--- 2. Preprocessing Data ---")
    if os.system("python utils/preprocess.py") != 0:
        print("Error in preprocessing")
        return
    
    print("\n--- 3. Training Freshness Model ---")
    if os.system("python training/train_freshness.py") != 0:
        print("Error in freshness training")
        return
    
    print("\n--- 4. Training Spoilage Model ---")
    if os.system("python training/train_spoilage.py") != 0:
        print("Error in spoilage training")
        return
    
    print("\n--- 5. Training Priority Model ---")
    if os.system("python training/train_priority.py") != 0:
        print("Error in priority training")
        return
    
    print("\n>>> PIPELINE COMPLETE <<<")

if __name__ == "__main__":
    run_all_training()
