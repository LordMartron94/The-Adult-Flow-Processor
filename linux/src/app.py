from src.merge_pipeline.merge_component_context import MergeComponentContext
from src.merge_pipeline.processing_pipeline import ProcessingPipeline


class App:
	def run(self):
		# ==== TESTING ====

		# tester = FileHandler()
		# results = tester.get_children_paths(Path("/media/mr-hoorn/Seagate External (HDD) [3.7TB]/Porn Streaming Cache/1. Recording/alodiefairall"), ".mp4")

		# print(f"Result:\n")
		# pprint.pp(results)

		# exit()
		
		# ==== STOP TESTING ====

		merge_context: MergeComponentContext = MergeComponentContext()
		app_pipeline: ProcessingPipeline = ProcessingPipeline(merge_context)
		app_pipeline.build_pipeline()
		app_pipeline.flow(None)
