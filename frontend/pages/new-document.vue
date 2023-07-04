<template>
    <div class="contain mx-auto flex flex-col space-y-12">
        <h1 class="text-4xl font-semibold text-center">New Document</h1>
      <div class="p-10 flex-none w-200 space-y-4">
        <select v-model="selectedBankTag" class="w-full p-3">
          <option v-for="bank in banks" :key="bank.tag" :value="bank.tag">
            {{ bank.name }}
          </option>
        </select>
        <h2 class="text-lg">Documents</h2>
        <ul>
          <li v-for="doc in documents" :key="doc">{{ doc }}</li>
        </ul>
        <input v-model="newDocumentUrl" type="url" class="border" /><button
          class="button-green"
          @click="onClickAddDocument"
        >
          Add Document
        </button>
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
  
  const { data: documents, refresh: refreshDocuments } = useAsyncData(
    "documents",
    () => $fetch(`${backend}/api/documents/${selectedBankTag.value}`),
    {
      transform: makeParser(documentsSchema),
      server: false,
      watch: [selectedBankTag],
    }
  );    
  
  const newDocumentUrl = ref("");
  async function onClickAddDocument() {
    const newDocumentName = newDocumentUrl.value.split("/").at(-1);
    await $fetch(`${backend}/api/documents`, {
      method: "POST",
      body: {
        url: newDocumentUrl.value,
        bank: selectedBankTag.value,
        name: newDocumentName,
      },
    });
    newDocumentUrl.value = "";
    await refreshDocuments();
  }
  
</script>
  