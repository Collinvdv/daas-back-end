<template>
    <ul>
        <li v-for="activity in activities" :key="activity.id">
            {{ activity.title }}
        </li>
    </ul>
</template>

<script>
    export default {
        data() {
            return {
                activities: []
            }
        },
        mounted() {
            this.fetchActivities();
        },
        methods: {
            async fetchActivities() {
                const res = await fetch('http://127.0.0.1:8000/activities')
                if (!res.ok) throw new Error(`HTTP ${res.status}`)
                const data = await res.json()
                this.activities = data.activities;
            }
        }
    }
</script>