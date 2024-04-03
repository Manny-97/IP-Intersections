import cv2
import os
import numpy as np

class ImageLoader:
    @staticmethod
    def load_image(file_path):
        return cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

class GraphExtractor:
    @staticmethod
    def extract_graph(image):
        # Example: Apply Canny edge detection
        edges = cv2.Canny(image, 50, 150)
        return edges

class JetExtractor:
    @staticmethod
    def extract_jet(image):
        # Example: Compute histograms of gradients
        sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        orientation = np.arctan2(sobely, sobelx)
        hist, bins = np.histogram(orientation.ravel(), bins=20, range=(-np.pi, np.pi))
        return hist

class EBGMFaceRecognition:
    def __init__(self, gallery_folder):
        self.gallery_folder = gallery_folder
        self.gallery_images, self.gallery_graphs, self.gallery_jets = self.load_gallery_images()

    def load_gallery_images(self):
        gallery_images = []
        gallery_graphs = []
        gallery_jets = []
        for filename in os.listdir(self.gallery_folder):
            if filename.endswith(".ppm"):
                image_path = os.path.join(self.gallery_folder, filename)
                image = ImageLoader.load_image(image_path)
                if image is not None:
                    graph = GraphExtractor.extract_graph(image)
                    jet = JetExtractor.extract_jet(image)
                    gallery_images.append(image)
                    gallery_graphs.append(graph)
                    gallery_jets.append(jet)
                else:
                    print(f"Failed to load image: {filename}")
        if not gallery_images:
            raise ValueError("No valid gallery images found in the specified folder.")
        return gallery_images, gallery_graphs, gallery_jets

    def recognize_face(self, probe_image):
        probe_graph = GraphExtractor.extract_graph(probe_image)
        probe_jet = JetExtractor.extract_jet(probe_image)
        similarities = self.compute_similarity(self.gallery_graphs, self.gallery_jets, probe_graph, probe_jet)
        match_percentages = [similarity * 100 for similarity in similarities]
        return match_percentages

    def compute_similarity(self, gallery_graphs, gallery_jets, probe_graph, probe_jet):
        similarities = []
        for gallery_graph, gallery_jet in zip(gallery_graphs, gallery_jets):
            graph_similarity = self.compute_graph_similarity(gallery_graph, probe_graph)
            jet_similarity = self.compute_jet_similarity(gallery_jet, probe_jet)
            similarity = graph_similarity + jet_similarity  # Combine graph and jet similarities
            similarities.append(similarity)

        # Normalize the similarity scores
        max_similarity = max(similarities)
        if max_similarity == 0:
            return [0] * len(similarities)
        normalized_similarities = [similarity / max_similarity for similarity in similarities]
        return normalized_similarities


    def compute_graph_similarity(self, gallery_graph, probe_graph):
        # Compute Mean Squared Error (MSE)
        mse = np.mean((gallery_graph - probe_graph) ** 2)
        # Normalize the MSE
        similarity = 1 / (1 + mse)
        return similarity

    def compute_jet_similarity(self, gallery_jet, probe_jet):
        # Example: Compute histogram intersection
        return cv2.compareHist(np.array([gallery_jet], dtype=np.float32), np.array([probe_jet], dtype=np.float32), cv2.HISTCMP_INTERSECT)

    def save_graphs(self, graphs, directory):
        os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist
        for i, graph in enumerate(graphs):
            filename = os.path.join(directory, f"graph_{i}.pgm.graphs")
            with open(filename, "w") as file:
                # Write the graph data to the file
                for row in graph:
                    file.write(' '.join(map(str, row)) + '\n')

    def save_jets(self, jets, directory):
        os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist
        for i, jet in enumerate(jets):
            filename = os.path.join(directory, f"jet_{i}.pgm.jets")
            with open(filename, "w") as file:
                # Write the jet data to the file
                file.write(' '.join(map(str, jet)) + '\n')



# Sample data
probe_image = ImageLoader.load_image("00001_930831_fa_a.ppm")

gallery_image = "input_images/00001"

# Create EBGMFaceRecognition instance with gallery images from "input_images" folder
ebgm_face_recognition = EBGMFaceRecognition(gallery_image)

# Recognize face
match_percentages = ebgm_face_recognition.recognize_face(probe_image)

directory = "output_images"

directory = "output_images"

# Save graphs and jets
ebgm_face_recognition.save_graphs(ebgm_face_recognition.gallery_graphs, directory)
ebgm_face_recognition.save_jets(ebgm_face_recognition.gallery_jets, directory)

# Print match percentages
for i, percentage in enumerate(match_percentages):
    print(f"Match percentage with image {i}: {percentage:.2f}%")
