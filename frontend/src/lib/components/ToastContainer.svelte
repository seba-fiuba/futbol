<script>
	import { toast } from '$lib/stores/toast';

	const stylesByType = {
		success: 'bg-green-600 text-white',
		error: 'bg-red-600 text-white',
		warning: 'bg-yellow-500 text-gray-900',
		info: 'bg-gray-800 text-white'
	};

	const iconByType = {
		success: '✅',
		error: '❌',
		warning: '⚠️',
		info: 'ℹ️'
	};
</script>

<div class="fixed top-4 right-4 z-[1000] flex flex-col gap-2 w-[calc(100%-2rem)] max-w-sm pointer-events-none">
	{#each $toast as item (item.id)}
		<div class="pointer-events-auto rounded-lg shadow-lg px-4 py-3 flex items-start gap-3 {stylesByType[item.type] || stylesByType.info}">
			<span class="text-lg leading-none mt-0.5">{iconByType[item.type] || iconByType.info}</span>
			<div class="flex-1 text-sm font-medium">{item.message}</div>
			<button
				type="button"
				on:click={() => toast.remove(item.id)}
				class="text-current/80 hover:text-current font-bold leading-none"
				aria-label="Cerrar notificacion"
			>
				×
			</button>
		</div>
	{/each}
</div>
