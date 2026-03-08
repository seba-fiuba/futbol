<script>
	import { onMount } from 'svelte';
	import { fetchEstadisticas, fetchJugadores, fetchEquipos } from '$lib/api';

	let estadisticas = [];
	let jugadores = [];
	let equipos = [];
	let loading = true;
	let error = null;

	onMount(async () => {
		try {
			[estadisticas, jugadores, equipos] = await Promise.all([
				fetchEstadisticas(),
				fetchJugadores(),
				fetchEquipos()
			]);
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	});

	function getJugadorNombre(jugadorId) {
		const jugador = jugadores.find((j) => j.id === jugadorId);
		return jugador ? jugador.nombre : 'Desconocido';
	}

	function getJugadorApodo(jugadorId) {
		const jugador = jugadores.find((j) => j.id === jugadorId);
		return jugador?.apodo || null;
	}

	function getJugadorImagen(jugadorId) {
		const jugador = jugadores.find((j) => j.id === jugadorId);
		return jugador?.imagen || null;
	}

	function getEquipoNombre(equipoId) {
		const equipo = equipos.find((e) => e.id === equipoId);
		return equipo ? equipo.nombre : 'Desconocido';
	}

	$: goleadores = estadisticas.reduce((acc, est) => {
		const existing = acc.find((g) => g.jugador_id === est.jugador_id);
		if (existing) {
			existing.goles += est.goles;
			existing.partidos += 1;
		} else {
			acc.push({
				jugador_id: est.jugador_id,
				goles: est.goles,
				partidos: 1
			});
		}
		return acc;
	}, []).sort((a, b) => b.goles - a.goles);
</script>

<svelte:head>
	<title>Tabla de Goleadores - Fútbol Manager</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<h1 class="text-3xl font-bold text-gray-800">🏆 Tabla de Goleadores</h1>
	</div>

	{#if loading}
		<div class="text-center py-12">
			<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
			<p class="mt-4 text-gray-600">Cargando estadísticas...</p>
		</div>
	{:else if error}
		<div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
			<p class="font-semibold">Error:</p>
			<p>{error}</p>
		</div>
	{:else if goleadores.length === 0}
		<div class="bg-gray-50 rounded-lg p-12 text-center">
			<p class="text-gray-600 text-lg">No hay estadísticas de goles registradas</p>
		</div>
	{:else}
		<!-- Podio Top 3 -->
		{#if goleadores.length >= 3}
			<div class="grid grid-cols-3 gap-4 mb-8">
				<!-- Segundo Lugar -->
				<div class="mt-8">
					<div class="bg-gradient-to-br from-gray-300 to-gray-400 rounded-lg p-6 text-center shadow-lg">
						<div class="text-4xl mb-2">🥈</div>
						{#if getJugadorImagen(goleadores[1].jugador_id)}
							<img 
								src={getJugadorImagen(goleadores[1].jugador_id)} 
								alt={getJugadorNombre(goleadores[1].jugador_id)}
								class="w-20 h-20 rounded-full object-cover mx-auto mb-3 border-4 border-white"
							/>
						{:else}
							<div class="w-20 h-20 rounded-full bg-white flex items-center justify-center text-4xl mx-auto mb-3 border-4 border-white">
								👤
							</div>
						{/if}
						<h3 class="font-bold text-gray-800 text-lg">{getJugadorNombre(goleadores[1].jugador_id)}</h3>
						{#if getJugadorApodo(goleadores[1].jugador_id)}
							<p class="text-sm text-gray-700">"{getJugadorApodo(goleadores[1].jugador_id)}"</p>
						{/if}
						<p class="text-3xl font-bold text-gray-800 mt-3">{goleadores[1].goles}</p>
						<p class="text-sm text-gray-700">goles</p>
					</div>
				</div>

				<!-- Primer Lugar -->
				<div>
					<div class="bg-gradient-to-br from-yellow-400 to-yellow-500 rounded-lg p-6 text-center shadow-2xl transform scale-105">
						<div class="text-5xl mb-2">🥇</div>
						{#if getJugadorImagen(goleadores[0].jugador_id)}
							<img 
								src={getJugadorImagen(goleadores[0].jugador_id)} 
								alt={getJugadorNombre(goleadores[0].jugador_id)}
								class="w-24 h-24 rounded-full object-cover mx-auto mb-3 border-4 border-white"
							/>
						{:else}
							<div class="w-24 h-24 rounded-full bg-white flex items-center justify-center text-5xl mx-auto mb-3 border-4 border-white">
								👤
							</div>
						{/if}
						<h3 class="font-bold text-gray-800 text-xl">{getJugadorNombre(goleadores[0].jugador_id)}</h3>
						{#if getJugadorApodo(goleadores[0].jugador_id)}
							<p class="text-sm text-gray-700">"{getJugadorApodo(goleadores[0].jugador_id)}"</p>
						{/if}
						<p class="text-4xl font-bold text-gray-800 mt-3">{goleadores[0].goles}</p>
						<p class="text-sm text-gray-700">goles</p>
						<div class="mt-3 text-2xl">👑</div>
					</div>
				</div>

				<!-- Tercer Lugar -->
				<div class="mt-8">
					<div class="bg-gradient-to-br from-orange-400 to-orange-500 rounded-lg p-6 text-center shadow-lg">
						<div class="text-4xl mb-2">🥉</div>
						{#if getJugadorImagen(goleadores[2].jugador_id)}
							<img 
								src={getJugadorImagen(goleadores[2].jugador_id)} 
								alt={getJugadorNombre(goleadores[2].jugador_id)}
								class="w-20 h-20 rounded-full object-cover mx-auto mb-3 border-4 border-white"
							/>
						{:else}
							<div class="w-20 h-20 rounded-full bg-white flex items-center justify-center text-4xl mx-auto mb-3 border-4 border-white">
								👤
							</div>
						{/if}
						<h3 class="font-bold text-gray-800 text-lg">{getJugadorNombre(goleadores[2].jugador_id)}</h3>
						{#if getJugadorApodo(goleadores[2].jugador_id)}
							<p class="text-sm text-gray-700">"{getJugadorApodo(goleadores[2].jugador_id)}"</p>
						{/if}
						<p class="text-3xl font-bold text-gray-800 mt-3">{goleadores[2].goles}</p>
						<p class="text-sm text-gray-700">goles</p>
					</div>
				</div>
			</div>
		{/if}

		<!-- Tabla Completa -->
		<div class="bg-white rounded-lg shadow-md overflow-hidden">
			<div class="overflow-x-auto">
				<table class="w-full">
					<thead class="bg-green-600 text-white">
						<tr>
							<th class="px-4 py-3 text-left text-sm font-semibold">Pos</th>
							<th class="px-4 py-3 text-left text-sm font-semibold">Jugador</th>
							<th class="px-4 py-3 text-center text-sm font-semibold">⚽ Goles</th>
							<th class="px-4 py-3 text-center text-sm font-semibold">Partidos</th>
							<th class="px-4 py-3 text-center text-sm font-semibold">Promedio</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200">
						{#each goleadores as goleador, i}
							<tr class="hover:bg-gray-50 transition-colors {i < 3 ? 'bg-yellow-50' : ''}">
								<td class="px-4 py-3 text-sm font-bold text-gray-700">
									{#if i === 0}
										🥇
									{:else if i === 1}
										🥈
									{:else if i === 2}
										🥉
									{:else}
										{i + 1}
									{/if}
								</td>
								<td class="px-4 py-3">
									<div class="flex items-center space-x-3">
										{#if getJugadorImagen(goleador.jugador_id)}
											<img 
												src={getJugadorImagen(goleador.jugador_id)} 
												alt={getJugadorNombre(goleador.jugador_id)}
												class="w-10 h-10 rounded-full object-cover"
											/>
										{:else}
											<div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-xl">
												👤
											</div>
										{/if}
										<div>
											<p class="font-semibold text-gray-800">{getJugadorNombre(goleador.jugador_id)}</p>
											{#if getJugadorApodo(goleador.jugador_id)}
												<p class="text-sm text-gray-600">"{getJugadorApodo(goleador.jugador_id)}"</p>
											{/if}
										</div>
									</div>
								</td>
								<td class="px-4 py-3 text-center text-lg font-bold text-green-600">
									{goleador.goles}
								</td>
								<td class="px-4 py-3 text-center text-sm text-gray-700">
									{goleador.partidos}
								</td>
								<td class="px-4 py-3 text-center text-sm font-semibold text-gray-700">
									{(goleador.goles / goleador.partidos).toFixed(2)}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>

		<!-- Estadísticas Totales -->
		<div class="bg-white rounded-lg shadow-md p-6">
			<h3 class="font-semibold text-gray-800 mb-4">Estadísticas Generales</h3>
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
				<div>
					<p class="text-3xl font-bold text-green-600">{goleadores.reduce((sum, g) => sum + g.goles, 0)}</p>
					<p class="text-gray-600">Goles Totales</p>
				</div>
				<div>
					<p class="text-3xl font-bold text-blue-600">{goleadores.length}</p>
					<p class="text-gray-600">Goleadores</p>
				</div>
				<div>
					<p class="text-3xl font-bold text-purple-600">
						{(goleadores.reduce((sum, g) => sum + g.goles, 0) / goleadores.reduce((sum, g) => sum + g.partidos, 0)).toFixed(2)}
					</p>
					<p class="text-gray-600">Promedio por Partido</p>
				</div>
			</div>
		</div>
	{/if}
</div>
