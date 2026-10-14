<template>
    <div>
        <h1>
            Counter {{ counterValue }}
        </h1>

        <button @click="addOne()">
            Add one
        </button>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                counterValue: 15
            }
        },
        methods: {
            addOne() {
                this.counterValue++;
            }
        }
    }
</script>