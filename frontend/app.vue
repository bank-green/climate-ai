<template>
  <div class="grid grid-cols-2 gap-3">
    <div>
      <h1>Question</h1>
      <select v-model="selectedQuestionId" class="max-w-full">
        <option
          v-for="question in questions"
          :key="question.id"
          :value="question.id"
        >
          {{ question.question }}
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
        <option v-for="bank in banks" :key="bank.tag" :value="bank.tag">
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
import { z, makeParser } from "@sidebase/nuxt-parse";
const config = useRuntimeConfig();
const backend = config.public.backend;

const banks = [
  { tag: "natwest", name: "NatWest" },
  { tag: "rbs", name: "Royal Bank of Scotland" },
];

const selectedBankTag = ref("rbs");

const documentsSchema = z.array(z.string());

const { data: documents } = useAsyncData(
  "documents",
  () => $fetch(`${backend}/api/documents/${selectedBankTag.value}`),
  {
    transform: makeParser(documentsSchema),
    server: false,
    watch: [selectedBankTag],
  }
);

const questionsSchema = z.array(
  z.object({
    id: z.number(),
    question: z.string(),
  })
);

const { data: questions } = useFetch(`${backend}/api/questions`, {
  transform: makeParser(questionsSchema),
  server: false,
});

const selectedQuestionId = ref(1);

const selectedQuestionText = computed(
  () =>
    questions.value!.find((q) => q.id === selectedQuestionId.value)?.question
);

const llmAnswer: Ref<null | string> = ref(
  `No, the policy prohibits new customer relationships with corporates who explore for, extract or produce coal, including those involved in the exploration and production of raw metal ores. (reference: excerpt under "Mining & Metals Risk Acceptance Criteria define the level of ESE risk the bank is prepared to accept, and our expectations of companies to manage ESE risks. This includes having relevant policies and procedures which demonstrate a good understanding of ESE issues and the capacity to manage these risks through good governance and controls. It also includes a positive track record of managing ESE risks and a commitment to transparency. Our policies reflect applicable national and international laws and take into account good international practice, for example managing climate change. They also incorporate a number of voluntary standards such as the Equator Principles and the UN Global Compact. We also expect our customers to adhere to local and international environmental, social and human rights standards. The policies apply to all legal entities within the Group.")`
);

const llmResponseSchema = z.object({
  response: z.string(),
});

async function onClickAsk() {
  const res = makeParser(llmResponseSchema)(
    await $fetch(`${backend}/api/query`, {
      method: "POST",
      body: {
        questionId: selectedQuestionId.value,
        bank: selectedBankTag.value,
      },
    })
  );
  llmAnswer.value = res.response;
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
