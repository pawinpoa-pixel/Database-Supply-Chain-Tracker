<template>
  <div class="timeline">
    <div
      v-for="entry in history"
      :key="entry.id"
      class="timeline-item"
    >
      <div class="circle">
        {{ icon(entry.status) }}
      </div>

      <div class="content">
        <h4>{{ formatStatus(entry.status) }}</h4>

        <p class="time">
          {{ formatDate(entry.status_timestamp) }}
        </p>

        <p v-if="entry.location">
          📍 {{ entry.location }}
        </p>

        <p v-if="entry.notes">
          {{ entry.notes }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  history: {
    type: Array,
    default: () => []
  }
})

function formatDate(value) {
  return value ? new Date(value).toLocaleString() : ""
}

function formatStatus(status) {
  return status.replace("_", " ").toUpperCase()
}

function icon(status) {
  switch (status) {
    case "pending":
      return "🟡"
    case "in_transit":
      return "🚚"
    case "delivered":
      return "✅"
    default:
      return "📦"
  }
}
</script>

<style scoped>
.timeline {
  margin-top: 20px;
}

.timeline-item {
  display: flex;
  gap: 15px;
  position: relative;
  padding-bottom: 25px;
}

.timeline-item:not(:last-child)::before {
  content: "";
  position: absolute;
  left: 15px;
  top: 34px;
  width: 2px;
  height: calc(100% - 10px);
  background: #d1d5db;
}

.circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #eef4ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.content h4 {
  margin: 0;
}

.time {
  color: gray;
  font-size: 0.85rem;
}
</style>