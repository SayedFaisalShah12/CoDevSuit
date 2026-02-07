import matplotlib.pyplot as plt
import numpy as np

class MetricsVisualizer:
    """
    Creates premium visualizations for code metrics.
    """
    @staticmethod
    def plot_complexity_distribution(complexity_data, output_path="complexity_dist.png"):
        """
        Plots a bar chart of complexity per function/method.
        """
        names = [item['name'] for item in complexity_data]
        values = [item['complexity'] for item in complexity_data]
        
        plt.figure(figsize=(10, 6))
        colors = plt.cm.viridis(np.linspace(0, 1, len(names)))
        bars = plt.bar(names, values, color=colors)
        
        plt.xlabel('Functions / Classes')
        plt.ylabel('Cyclomatic Complexity')
        plt.title('Code Complexity Distribution')
        plt.xticks(rotation=45, ha='right')
        
        # Add labels on top of bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, yval, ha='center', va='bottom')
            
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        return output_path

    @staticmethod
    def plot_maintainability_gauge(mi_score, output_path="maintainability_gauge.png"):
        """
        Plots a 'gauge' or simple color indicator for Maintainability Index.
        """
        plt.figure(figsize=(6, 2))
        color = 'green' if mi_score > 50 else 'orange' if mi_score > 20 else 'red'
        
        plt.barh(['Maintainability'], [mi_score], color=color)
        plt.xlim(0, 100)
        plt.title(f'Maintainability Index: {mi_score:.2f}')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        return output_path
