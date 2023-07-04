<template>
    <div class="container mx-auto flex flex-col items-center space-y-12">
        
        <h1 class="text-4xl font-semibold">New Question</h1>
        <div class="flex flex-col md:flex-row gap-2 w-full">
          <input
            v-model="newQuestion"
            class="relative w-full appearance-none border bg-white rounded-2xl shadow-sm px-8 py-4 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-sushi-500 focus:border-sushi-500 text-md truncate"
            :class="{
                'border-white': !newQuestion,
                'border-sushi-100': newQuestion,
            }"
            placeholder="Enter your question here"
          />
          <button class="button-green md:w-48" @click="onClickAddQuestion">Add Question</button>
          </div>
        <MatchedQuestionList
          :search="newQuestion"
          :questions="questions"
        />
    </div>
</template>
<script setup lang="ts">
import { z, makeParser } from "@sidebase/nuxt-parse";
import { Question } from "~/utils/backendInterfaces";


const config = useRuntimeConfig();
const backend = config.public.backend;
  
const questionsSchema = z.array(
  z.object({
    id: z.number(),
    question: z.string(),
  })
);

const { data: questions, refresh: refreshQuestions } = useFetch<Question[]>(
  `${backend}/api/questions`,
  {
    transform: makeParser(questionsSchema),
    server: false,
  }
);

const newQuestion = ref("");

async function onClickAddQuestion() {
  await $fetch(`${backend}/api/questions`, {
    method: "POST",
    body: {
      newQuestion: newQuestion.value,
    },
  });
  newQuestion.value = "";
  await refreshQuestions();
}
</script>