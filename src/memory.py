import json
import os

class CustomerInteractionMemory:
    def __init__(self, memory_dir="C:\\AI_CRM_project\\data\\memory"):
        self.memory_dir = memory_dir
        os.makedirs(self.memory_dir, exist_ok=True)

    def _get_profile_path(self, customer_id: str) -> str:
        return os.path.join(self.memory_dir, f"{customer_id}_memory.json")

    def get_context(self, customer_id: str) -> dict:
        """Retrieves both short-term thread items and long-term behavioral preferences."""
        path = self._get_profile_path(customer_id)
        if not os.path.exists(path):
            return {
                "short_term_buffer": [],
                "long_term_preferences": "No established historic preferences recorded yet."
            }
        with open(path, "r") as f:
            return json.load(f)

    def save_interaction(self, customer_id: str, human_msg: str, ai_msg: str, summary_update: str = None):
        """Appends recent dialogue to short-term buffer and updates long-term flags."""
        context = self.get_context(customer_id)
        
        # Append to short-term sliding context window
        context["short_term_buffer"].append({
            "user": human_msg,
            "assistant": ai_msg
        })
        
        # Trim sliding window buffer to keep only the last 3 interactions (short-term window constraint)
        if len(context["short_term_buffer"]) > 3:
            context["short_term_buffer"] = context["short_term_buffer"][-3:]
            
        if summary_update:
            context["long_term_preferences"] = summary_update

        with open(self._get_profile_path(customer_id), "w") as f:
            json.dump(context, f, indent=4)
