<script>
	import { onMount } from 'svelte';
	import { fetchPartidos, fetchEquipos } from '$lib/api';

	let partidos = [];
	let equipos = [];
	let loading = true;
	let error = null;

	onMount(async () => {
		try {
			[partidos, equipos] = await Promise.all([fetchPartidos(), fetchEquipos()]);
			// Ordenar por fecha descendente
			partidos = partidos.sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	});

	function getEquipoNombre(equipoId) {
		const equipo = equipos.find((e) => e.id === equipoId);
		return equipo ? equipo.nombre : 'Desconocido';
	}

	function formatFecha(fecha) {
		return new Date(fecha).toLocaleDateString('es-AR', {
			day: '2-digit',
			month: '2-digit',
			year: 'numeric'
		});
	}
</script>

<svelte:head>
	<title>Partidos - Fútbol Manager</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
		<h1 class="text-2xl md:text-3xl font-bold text-gray-800">⚽ Partidos</h1>
		<a
			href="/partidos/nuevo"
			class="w-full sm:w-auto bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-3 rounded-lg shadow-md hover:shadow-lg transition-all flex items-center justify-center space-x-2"
		>
			<span class="text-xl">➕</span>
			<span>Nuevo Partido</span>
		</a>
	</div>

	{#if loading}
		<div class="text-center py-12">
			<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
			<p class="mt-4 text-gray-600">Cargando partidos...</p>
		</div>
	{:else if error}
		<div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
			<p class="font-semibold">Error:</p>
			<p>{error}</p>
		</div>
	{:else if partidos.length === 0}
		<div class="bg-gray-50 rounded-lg p-12 text-center">
			<p class="text-gray-600 text-lg mb-4">No hay partidos registrados</p>
			<a
				href="/partidos/nuevo"
				class="inline-block bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-3 rounded-lg"
			>
				Registrar primer partido
			</a>
		</div>
	{:else}
		<div class="grid grid-cols-1 gap-4">
			{#each partidos as partido}
				<div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden">
					<div class="p-6">
						<div class="flex items-center justify-between mb-4">
							<span class="text-sm text-gray-600 font-medium">{formatFecha(partido.fecha)}</span>
							<a
								href="/partidos/{partido.id}/editar"
								class="text-blue-600 hover:text-blue-800 text-sm font-medium"
							>
								Editar
							</a>
						</div>
						
			<!-- Desktop View -->
			<div class="hidden md:grid grid-cols-7 gap-4 items-center">
							<!-- Equipo Local -->
							<div class="col-span-3 text-right">
								<h3 class="text-xl font-bold text-gray-800">{getEquipoNombre(partido.equipo_local_id)}</h3>
								<span class="text-sm text-gray-600">Local</span>
							</div>

							<!-- Score -->
							<div class="col-span-1 text-center">
								<div class="flex items-center justify-center space-x-3">
									<span class="text-3xl font-bold text-green-600">{partido.goles_local}</span>
									<span class="text-2xl text-gray-400">-</span>
									<span class="text-3xl font-bold text-green-600">{partido.goles_visitante}</span>
								</div>
							</div>

							<!-- Equipo Visitante -->
							<div class="col-span-3 text-left">
								<h3 class="text-xl font-bold text-gray-800">{getEquipoNombre(partido.equipo_visitante_id)}</h3>
								<span class="text-sm text-gray-600">Visitante</span>
							</div>
						</div>

						<!-- Mobile View -->
						<div class="md:hidden">
							<div class="flex items-center justify-between mb-3">
								<div class="flex-1">
									<h3 class="font-bold text-gray-800">{getEquipoNombre(partido.equipo_local_id)}</h3>
									<span class="text-xs text-gray-600">Local</span>
								</div>
								<div class="flex items-center space-x-2 px-4">
									<span class="text-2xl font-bold text-green-600">{partido.goles_local}</span>
									<span class="text-xl text-gray-400">-</span>
									<span class="text-2xl font-bold text-green-600">{partido.goles_visitante}</span>
								</div>
								<div class="flex-1 text-right">
									<h3 class="font-bold text-gray-800">{getEquipoNombre(partido.equipo_visitante_id)}</h3>
									<span class="text-xs text-gray-600">Visitante</span>
								</div>
							</div>
						</div>

						{#if partido.goles_local > partido.goles_visitante}
							<div class="mt-4 text-center text-sm text-gray-600">
								🏆 Victoria {getEquipoNombre(partido.equipo_local_id)}
							</div>
						{:else if partido.goles_visitante > partido.goles_local}
							<div class="mt-4 text-center text-sm text-gray-600">
								🏆 Victoria {getEquipoNombre(partido.equipo_visitante_id)}
							</div>
						{:else}
							<div class="mt-4 text-center text-sm text-gray-600">
								🤝 Empate
							</div>
						{/if}
					</div>
				</div>
			{/each}
		</div>

		<div class="text-center text-gray-600">
			Total de partidos: {partidos.length}
		</div>
	{/if}
</div>
