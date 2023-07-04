<template>
    <div v-if="matchedQuestions.length > 0" class="flex flex-col items-center w-full">
        <p class="font-semibold text-md">Please check if your question is already added</p>
        <ol class="space-y-6 w-full mt-6">
            <li v-for="_q in matchedQuestions" :key="_q.item.id" class="block py-4 px-12 rounded-2xl shadow-sm bg-white transition duration-150 ease-in-out hover:bg-gray-50 border border-transparent hover:border-sushi-500">
            {{ _q.item.question }}
            </li>
        </ol>
    </div>
</template>
<script setup lang="ts">
import Fuse from 'fuse.js';
import { Question } from "~/utils/backendInterfaces";

const props = withDefaults(
    defineProps<{
        search: string;
        questions: Question[] | null;
        resultLimit?: number | null;
    }>(),
    {
        resultLimit: 5,
    }   
);

// Refine search results by modifying values
// read more at https://fusejs.io/concepts/scoring-theory.html#scoring-theory
const fuseOptions = {
    includeScore: false,
    threshold: 0.2,
    ignoreLocation: true,
    keys: ['question']
}

const matchedQuestions = computed(() => {
    if (props.search.length == 0 || props.questions == null) return [];
    let _fuse = new Fuse(props.questions, fuseOptions);
    const results : any[] = _fuse.search(props.search);
    return props.resultLimit ? results.splice(0, props.resultLimit) : results;
})
</script>