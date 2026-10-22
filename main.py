import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def assign_grade(average):
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


def main():
    try:
        df = pd.read_csv("students.csv", skipinitialspace=True)
        df.columns = df.columns.str.strip().str.lower()

        required_columns = ["name", "math", "science", "english"]

        if not all(column in df.columns for column in required_columns):
            raise ValueError(
                "Required columns: name, math, science, english"
            )

        if df.empty:
            raise ValueError("No student records found.")

        df = df[required_columns].copy()
        df["name"] = df["name"].astype("string").str.strip()

        if df["name"].isna().any() or df["name"].eq("").any():
            raise ValueError("Every student must have a name.")

        subjects = ["math", "science", "english"]

        for subject in subjects:
            df[subject] = pd.to_numeric(df[subject], errors="raise")

        if df[subjects].isna().any().any():
            raise ValueError("Marks cannot be empty.")

        if not df[subjects].map(
            lambda x: pd.notna(x) and 0 <= x <= 100
        ).all().all():
            raise ValueError("Marks must be between 0 and 100.")

        df["average"] = df[subjects].mean(axis=1).round(2)

        print("\nSUBJECT-WISE ANALYSIS")

        for subject in subjects:
            print(
                subject.capitalize(),
                "Average:",
                round(df[subject].mean(), 2)
            )

        df["grade"] = df["average"].apply(assign_grade)

        df["status"] = df[subjects].ge(40).all(axis=1).map({
            True: "Pass",
            False: "Fail"
        })

        print("\nSTUDENT PERFORMANCE REPORT")
        print("-" * 75)
        print(df.to_string(index=False))

        print("\nClass Average:", round(df["average"].mean(), 2))

        top_student = df.loc[df["average"].idxmax()]
        print("Top Student:", top_student["name"])
        print("Top Average:", top_student["average"])

        df.to_csv("performance_report.csv", index=False)

        import numpy as np

        x = np.arange(len(df["name"]))
        width = 0.25

        plt.figure(figsize=(10, 6))

        math_bars = plt.bar(
            x - width, df["math"], width,
            label="Math", color="#3498DB", edgecolor="black"
        )

        science_bars = plt.bar(
            x, df["science"], width,
            label="Science", color="#2ECC71", edgecolor="black"
        )

        english_bars = plt.bar(
            x + width, df["english"], width,
            label="English", color="#E67E22", edgecolor="black"
        )

        plt.title("Student Subject-Wise Comparison",
                  fontsize=16, fontweight="bold")
        plt.xlabel("Students")
        plt.ylabel("Marks (%)")
        plt.xticks(x, df["name"])
        plt.ylim(0, 110)
        plt.yticks(range(0, 101, 10))
        plt.grid(axis="y", linestyle="--", alpha=0.4)
        plt.gca().set_axisbelow(True)
        plt.legend()

        for bars in [math_bars, science_bars, english_bars]:
            for bar in bars:
                height = bar.get_height()
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 1,
                    f"{height:.0f}",
                    ha="center",
                    va="bottom",
                    fontsize=8
                )

        plt.tight_layout()
        plt.savefig("student_performance.png", dpi=300,
                    bbox_inches="tight")
        plt.show()
        subject_averages = df[subjects].mean()

        plt.figure(figsize=(8, 5))

        bars = plt.bar(
            subject_averages.index.str.capitalize(),
            subject_averages.values,
            color=["#3498DB", "#2ECC71", "#E67E22"],
            edgecolor="black",
            width=0.6
        )

        plt.title("Subject-Wise Average Marks",
                  fontsize=16, fontweight="bold")
        plt.xlabel("Subjects")
        plt.ylabel("Average Marks (%)")
        plt.ylim(0, 110)
        plt.yticks(range(0, 101, 10))
        plt.grid(axis="y", linestyle="--", alpha=0.4)
        plt.gca().set_axisbelow(True)

        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height + 1,
                f"{height:.2f}",
                ha="center",
                va="bottom",
                fontweight="bold"
            )

        plt.tight_layout()
        plt.savefig("subject_average_comparison.png",
                    dpi=300, bbox_inches="tight")
        plt.show()

        print("Subject average chart saved to subject_average_comparison.png")
        subject_averages = df[subjects].mean()

        plt.figure(figsize=(9, 6))

        bars = plt.bar(
            ["Math", "Science", "English"],
            subject_averages.values,
            color=["#3498DB", "#2ECC71", "#E67E22"],
            edgecolor="black",
            width=0.6
        )

        plt.title(
            "Subject-Wise Performance Comparison",
            fontsize=16,
            fontweight="bold",
            pad=18
        )

        plt.xlabel("Subjects", fontsize=12)
        plt.ylabel("Average Marks (%)", fontsize=12)
        plt.ylim(0, 110)
        plt.yticks(range(0, 101, 10))
        plt.grid(axis="y", linestyle="--", alpha=0.4)
        plt.gca().set_axisbelow(True)

        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height + 1,
                f"{height:.2f}",
                ha="center",
                va="bottom",
                fontweight="bold"
            )

        plt.tight_layout()
        plt.savefig("subject_comparison.png", dpi=300, bbox_inches="tight")
        plt.show()

        print("Subject comparison chart saved to subject_comparison.png")

        print("\nReport saved to performance_report.csv")
        print("Chart saved to student_performance.png")

    except FileNotFoundError:
        print("Error: students.csv was not found.")

    except pd.errors.EmptyDataError:
        print("Error: students.csv is empty.")

    except (ValueError, TypeError, pd.errors.ParserError) as error:
        print("Data error:", error)


if __name__ == "__main__":
    main()