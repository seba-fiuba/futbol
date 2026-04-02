import { writable } from 'svelte/store';

const DEFAULT_DURATION = 3500;

function createToastStore() {
	const { subscribe, update } = writable([]);

	function push(message, type = 'info', duration = DEFAULT_DURATION) {
		const id = crypto.randomUUID();
		update((toasts) => [...toasts, { id, message, type }]);

		if (duration > 0) {
			setTimeout(() => remove(id), duration);
		}

		return id;
	}

	function remove(id) {
		update((toasts) => toasts.filter((toast) => toast.id !== id));
	}

	return {
		subscribe,
		push,
		remove,
		success: (message, duration = DEFAULT_DURATION) => push(message, 'success', duration),
		error: (message, duration = DEFAULT_DURATION) => push(message, 'error', duration),
		info: (message, duration = DEFAULT_DURATION) => push(message, 'info', duration),
		warning: (message, duration = DEFAULT_DURATION) => push(message, 'warning', duration)
	};
}

export const toast = createToastStore();
