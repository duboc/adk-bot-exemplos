# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from typing import Optional
from google.genai import types

from google.adk.models import LLMRegistry

def _create_website_content(website_result: dict) -> types.Content:
    """Creates a types.Content object from website search results."""

    parts = [
        types.Part.from_text(text=f"Website Title: {website_result['title']}"),
        types.Part.from_uri(file_uri=website_result['link'], mime_type='text/html')
    ]

    return types.Content(role='user', parts=parts)


def add_website_content_in_request_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Modifies the LLM request to add website content."""

    website_search_result = []
    last_user_content = None
    if llm_request.contents and llm_request.contents[-1].role == 'user':
        last_user_content = llm_request.contents[-1]

    if (last_user_content and
        last_user_content.parts and
        last_user_content.parts[0].function_response and
        last_user_content.parts[0].function_response.name == "vertex_ai_website_search_tool"):
        website_search_result = last_user_content.parts[0].function_response.response

    if website_search_result:
        print("[Callback] Website Search content found. Adding content to LLM request.")
        for website_result_item in website_search_result['results']:
            website_content_to_add = _create_website_content(website_result_item['document']['derivedStructData'])
            llm_request.contents.append(website_content_to_add)

    print("[Callback] Proceeding with LLM call.")
    return None


    LLMRegistry()