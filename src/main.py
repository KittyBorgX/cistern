from api import get_workflow_job_id

def main():
    pr_num = int(input("Enter the PR Number> "))
    get_workflow_job_id(pr_num)

if __name__ == "__main__": 
    main()