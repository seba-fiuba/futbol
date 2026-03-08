<script>
	import { onMount } from 'svelte';
	import { fetchJugadores } from '$lib/api';

	let jugadores = [];
	let loading = true;
	let error = null;
	let searchTerm = '';

	onMount(async () => {
		try {
			jugadores = await fetchJugadores();
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	});

	$: filteredJugadores = jugadores.filter((j) =>
		j.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
		(j.apodo && j.apodo.toLowerCase().includes(searchTerm.toLowerCase()))
	);
</script>

<svelte:head>
	<title>Jugadores - Fútbol Manager</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<h1 class="text-3xl font-bold text-gray-800">👥 Jugadores</h1>
	</div>

	<!-- Search Bar -->
	<div class="bg-white rounded-lg shadow-md p-4">
		<input
			type="text"
			bind:value={searchTerm}
			placeholder="Buscar jugador por nombre o apodo..."
			class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
		/>
	</div>

	{#if loading}
		<div class="text-center py-12">
			<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
			<p class="mt-4 text-gray-600">Cargando jugadores...</p>
		</div>
	{:else if error}
		<div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
			<p class="font-semibold">Error:</p>
			<p>{error}</p>
		</div>
	{:else if filteredJugadores.length === 0}
		<div class="bg-gray-50 rounded-lg p-12 text-center">
			<p class="text-gray-600 text-lg">
				{searchTerm ? 'No se encontraron jugadores' : 'No hay jugadores registrados'}
			</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
			{#each filteredJugadores as jugador}
				<div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden">
					<div class="bg-gradient-to-br from-green-500 to-green-600 h-32 flex items-center justify-center">
						{#if jugador.imagen}
							<img src={jugador.imagen} alt={jugador.nombre} class="w-24 h-24 rounded-full object-cover border-4 border-white" />
						{:else}
							<div class="w-24 h-24 rounded-full bg-white flex items-center justify-center text-4xl border-4 border-white">
								👤
							</div>
						{/if}
					</div>
					<div class="p-4">
						<h3 class="text-xl font-bold text-gray-800 text-center">{jugador.nombre}</h3>
						{#if jugador.apodo}
							<p class="text-gray-600 text-center mt-1">"{jugador.apodo}"</p>
						{/if}
						<div class="mt-4 pt-4 border-t border-gray-200">
							<p class="text-sm text-gray-600 text-center">ID: {jugador.id}</p>
						</div>
					</div>
				</div>
			{/each}
		</div>

		<div class="text-center text-gray-600">
			Mostrando {filteredJugadores.length} de {jugadores.length} jugadores
		</div>
	{/if}
</div>
