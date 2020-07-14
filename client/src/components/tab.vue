<template>
    <div v-show="isActive"><slot></slot></div>
</template>

<script>
export default {
    name: 'tab',
    props: {
        name: {required: true},
        selected: {default: false}
    },
    data() {
        return {
            isActive: false
        }
    },
    mounted() {
        this.isActive = this.selected;
    },
    computed: {
        href() {
            return '#' + this.name.toLowerCase().replace(/ /g, '-');
        }
    }
}
</script>
