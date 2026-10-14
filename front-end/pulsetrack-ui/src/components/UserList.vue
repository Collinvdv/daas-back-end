<!-- We use this to display stuff: mustache {{ }}, v-for, v-if, @clic -->
<template>
    <div>
        <h1>
            Users ({{ users.length }})
        </h1>

        <button @click="toggleUsersHidden()">
            Show users
        </button>

        <ul v-if="!usersHidden">
            <li v-for="user in users">
                Name: {{ user.display_name }} <br>
                Email: {{ user.email }}
                <button @click="deleteUser(user.id)">
                    Delete
                </button>
            </li>
        </ul>
    </div>
</template>

<!-- Functionalities: data(), methods:, mounted() -->
<script>
    export default {
        data() {
            return {
                users: [],
                usersHidden: true
            }
        },
        async mounted() {
            const res = await fetch('http://127.0.0.1:8000/users')
            if (!res.ok) throw new Error(`HTTP ${res.status}`)
            const data = await res.json()
            this.users = data.users;
        },
        methods: {
            toggleUsersHidden() {
                this.usersHidden = !this.usersHidden;
            },
            async deleteUser(id) {
                const res = await fetch(`http://127.0.0.1:8000/users/${id}`, { method: 'DELETE' })
                if (!res.ok) throw new Error(`HTTP ${res.status}`)
                this.users = this.users.filter(user => user.id !== id);
            }
        }
    }
</script>