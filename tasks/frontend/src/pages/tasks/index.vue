<template>
  <v-card>
    <v-card-title>
      <v-breadcrumbs :items="[{ title: 'Tasks' }]" class="py-1 px-0 v-label" />
    </v-card-title>
    <v-card-text>
      <TaskList />
    </v-card-text>
  </v-card>
</template>
