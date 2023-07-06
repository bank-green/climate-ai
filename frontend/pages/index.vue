<template>
  <div class="contain mx-auto flex flex-col items-center space-y-6">
    <div class="flex flex-cols md:flex-rows w-full gap-1">
      <select v-model="selectedBankTag" class="">
        <option v-for="bank in banks" :key="bank.tag" :value="bank.tag">
          {{ bank.name }}
        </option>
      </select>

      <select v-model="selectedQuestionId" class="w-3/4">
        <option :value="-1" disabled selected>Select your option</option>
        <option
          v-for="question in questions"
          :key="question.id"
          :value="question.id"
        >
          {{ question.question }}
        </option>
      </select>

      <button class="button-green md:w-36" @click="onClickAsk">Ask</button>
    </div>
    <div v-if="answerState === 'ready'">
      <p class="p-10">
        Please select a bank, select a question, and click "Ask".
      </p>
    </div>
    <div v-else-if="answerState === 'loading'">
      <p class="p-10">Waiting for LLM response…</p>
    </div>
    <div v-else id="answer" class="rounded-xl bg-white p-6 scroll-mt-32">
      <h2 class="text-lg mb-3">Question:</h2>
      <p class="italic mb-3">{{ selectedQuestionText }}</p>
      <h2 class="mb-3 text-lg">Text excerpts provided to LLM:</h2>
      <blockquote
        v-for="chunk in chunks"
        :key="chunk"
        class="whitespace-pre-wrap ml-5 mb-5 text-sm"
      >
        {{ chunk }}
      </blockquote>
      <h2 class="mb-3 text-lg">LLM Answer</h2>
      <blockquote class="italic ml-5 mb-3">{{ llmAnswer }}</blockquote>

      <div v-if="llmAnswer" class="mb-3">
        <h2 class="mb-3 text-lg">Human Answer</h2>
        <p class="italic mb-3">{{ selectedQuestionText }}</p>
        <button
          class="rounded-full bg-slate-300 p-3 m-3"
          @click="onHumanAnswerClick('yes')"
        >
          Yes
        </button>
        <button
          class="rounded-full bg-slate-300 p-3 m-3"
          @click="onHumanAnswerClick('no')"
        >
          No
        </button>
        <span>{{ humanAnswer }}</span>
      </div>
      <div v-if="humanAnswer" class="mb-3">
        <h2 class="mb-3 text-lg">Feedback</h2>
        <p class="italic mb-3">How did the LLM do?</p>
        <button
          class="rounded-full bg-slate-300 p-3 m-3"
          @click="onLlmFeedback('great')"
        >
          Great
        </button>
        <button
          class="rounded-full bg-slate-300 p-3 m-3"
          @click="onLlmFeedback('poor')"
        >
          Poor
        </button>
        <span>{{ llmFeedback }}</span>
      </div>
      <div v-if="llmFeedback">
        <h2 class="mb-3 text-lg">Submit</h2>
        <button class="rounded-full bg-slate-300 p-3 m-3" @click="onSubmit">
          Submit
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { z, makeParser } from "@sidebase/nuxt-parse";
const config = useRuntimeConfig();
const backend = config.public.backend;

const banksSchema = z.array(
  z.object({
    tag: z.string(),
    name: z.string(),
  })
);

const { data: banks } = useFetch(`${backend}/api/banks`, {
  transform: makeParser(banksSchema),
  server: false,
});

const selectedBankTag = ref("natwest");

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

const defaultSelectedQuestionId = -1;
const selectedQuestionId = ref(defaultSelectedQuestionId);
const selectedQuestionText = computed(
  () =>
    questions.value?.find((q) => q.id === selectedQuestionId.value)?.question ??
    ""
);

const llmAnswer: Ref<null | string> = ref(
  `No, the policy prohibits new customer relationships with corporates who explore for, extract or produce coal, including those involved in the exploration and production of raw metal ores. (reference: excerpt under "Mining & Metals Risk Acceptance Criteria define the level of ESE risk the bank is prepared to accept, and our expectations of companies to manage ESE risks. This includes having relevant policies and procedures which demonstrate a good understanding of ESE issues and the capacity to manage these risks through good governance and controls. It also includes a positive track record of managing ESE risks and a commitment to transparency. Our policies reflect applicable national and international laws and take into account good international practice, for example managing climate change. They also incorporate a number of voluntary standards such as the Equator Principles and the UN Global Compact. We also expect our customers to adhere to local and international environmental, social and human rights standards. The policies apply to all legal entities within the Group.")`
);

const chunks: Ref<null | string[]> = ref(null);

const llmResponseSchema = z.object({
  response: z.string(),
  chunks: z.array(z.string()),
});

const answerState: Ref<"ready" | "loading" | "done"> = ref("ready");

async function onClickAsk() {
  answerState.value = "loading";
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
  chunks.value = res.chunks;
  answerState.value = "done";
  nextTick(() => {
    document.getElementById("answer")?.scrollIntoView();
  });
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
  answerState.value = "ready";
}
</script>
