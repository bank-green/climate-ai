<template>
  <div class="grid grid-cols-2 gap-3">
    <div>
      <h1>Question</h1>
      <select v-model="selectedQuestionId">
        <option
          v-for="question in questions"
          :key="question.id"
          :value="question.id"
        >
          {{ question.text }}
        </option>
      </select>
      <button @click="onClickAsk">Ask</button>
      <div v-if="llmAnswer">
        <p>Asked LLM: "{{ selectedQuestionText }}"</p>
        <p>{{ llmAnswer }}</p>

        <p>What's the answer to "{{ selectedQuestionText }}?"</p>
        <button @click="onHumanAnswerClick('yes')">Yes</button>
        <button @click="onHumanAnswerClick('no')">No</button>
        <div v-if="humanAnswer">
          <p>How did the LLM do?"</p>
          <button @click="onLlmFeedback('great')">Great</button>
          <button @click="onLlmFeedback('poor')">Poor</button>
        </div>
        <div v-if="llmFeedback">
          <button @click="onSubmit">Submit</button>
        </div>
      </div>
    </div>
    <div>
      <h1>Banks</h1>
      <select v-model="selectedBankTag">
        <option v-for="bank in banks" :key="bank.tag" :value="bank.name">
          {{ bank.name }}
        </option>
      </select>
      <h2>Documents</h2>
      <ul>
        <li v-for="doc in documents" :key="doc">{{ doc }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
const questions = [
  { id: 1, text: "Sample Question 1" },
  { id: 2, text: "Sample Question 2" },
];
const banks = [
  { tag: "natwest", name: "NatWest" },
  { tag: "rbs", name: "Royal Bank of Scotland" },
];

const documents = ["mining", "power"];
const selectedQuestionId = 1;
const selectedBankTag = banks[0].tag;
const selectedQuestionText = computed(
  () => questions.find((q) => q.id === selectedQuestionId)?.text
);
const llmAnswer: Ref<null | string> = ref(null);

function onClickAsk() {
  llmAnswer.value = "This is where an answer would be!";
}

type HumanAnswer = "yes" | "no";
const humanAnswer: Ref<null | HumanAnswer> = ref(null);
function onHumanAnswerClick(answer: HumanAnswer) {
  humanAnswer.value = answer;
}

type LlmFeedback = "great" | "poor";
const llmFeedback: Ref<null | LlmFeedback> = ref(null);
function onLlmFeedback(feedback: LlmFeedback) {
  llmFeedback.value = feedback;
}

function onSubmit() {
  llmAnswer.value = null;
  humanAnswer.value = null;
  llmFeedback.value = null;
}
</script>
